import requests

class ConfluenceTable:
    def __init__(self, username, password, base_url, page_id):
        self.username = username
        self.password = password
        self.base_url = base_url
        self.page_id = page_id

    def fetch_page_content(self):
        """
        Fetches the existing page content from Confluence API.
        """
        url = f'{self.base_url}/rest/api/content/{self.page_id}?expand=body.storage'
        headers = {"Accept": "application/json"}
        response = requests.get(url, auth=(self.username, self.password), headers=headers)
        response.raise_for_status()
        return response.json()

    def parse_table_data(self, page_data):
        """
        Parses the existing table data from the page content.
        """
        existing_table_data = [
            row.split('|') for row in page_data['body']['storage']['value'].split('\n')
            if row.startswith('|')
        ]
        return existing_table_data

    def convert_to_csf(self, table_data):
        """
        Converts the table data to Confluence Storage Format (CSF).
        """
        csf_data = "{table}" + "\n".join(["|".join(row) + "|" for row in table_data]) + "{table}"
        return csf_data

    def update_table(self, new_row):
        """
        Updates the existing table with the new row and saves the updated table to Confluence.
        """
        try:
            # Fetch existing table data
            page_data = self.fetch_page_content()
            existing_table_data = self.parse_table_data(page_data)

            # Update table data with new row
            updated_table_data = existing_table_data + [new_row]

            # Convert updated table data to CSF
            csf_data = self.convert_to_csf(updated_table_data)

            # Update page content with updated table data
            url = f'{self.base_url}/rest/api/content/{self.page_id}'
            headers = {"Accept": "application/json", "Content-Type": "application/json"}
            payload = {
                "id": self.page_id,
                "type": "page",
                "title": page_data['title'],
                "body": {
                    "storage": {
                        "value": csf_data,
                        "representation": "storage"
                    }
                },
                "version": {
                    "number": page_data['version']['number'] + 1,
                    "minorEdit": True
                }
            }
            response = requests.put(url, auth=(self.username, self.password), headers=headers, json=payload)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ValueError(f"Failed to update table. {str(e)}")


