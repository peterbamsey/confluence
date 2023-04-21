import unittest
from unittest.mock import MagicMock
from confluence_table import ConfluenceTable

class TestConfluenceTable(unittest.TestCase):
    def setUp(self):
        self.username = 'test_user'
        self.password = 'test_password'
        self.base_url = 'https://test.confluence.com'
        self.page_id = '123456789'
        self.table = ConfluenceTable(self.username, self.password, self.base_url, self.page_id)
        self.mock_fetch_page_content = MagicMock(return_value={
            'title': 'Test Page',
            'version': {'number': 2},
            'body': {
                'storage': {'value': '|Header 1|Header 2|\n|Value 1|Value 2|'}
            }
        })
        self.table.fetch_page_content = self.mock_fetch_page_content

    def test_fetch_page_content(self):
        # Mock HTTP response
        response = MagicMock()
        response.json.return_value = {'test': 'data'}
        response.raise_for_status.return_value = None
        self.table.requests.get = MagicMock(return_value=response)

        # Test method
        result = self.table.fetch_page_content()

        # Assertions
        self.table.requests.get.assert_called_once_with(
            f'{self.base_url}/rest/api/content/{self.page_id}?expand=body.storage',
            auth=(self.username, self.password),
            headers={"Accept": "application/json"}
        )
        self.assertEqual(result, {'test': 'data'})

    def test_parse_table_data(self):
        # Test method
        result = self.table.parse_table_data(self.mock_fetch_page_content.return_value)

        # Assertions
        self.assertEqual(result, [['Header 1', 'Header 2'], ['Value 1', 'Value 2']])

    def test_convert_to_csf(self):
        # Test method
        result = self.table.convert_to_csf([['Header 1', 'Header 2'], ['Value 1', 'Value 2']])

        # Assertions
        self.assertEqual(result, "{table}\n|Header 1|Header 2|\n|Value 1|Value 2|\n{table}")

    def test_update_table(self):
        # Mock HTTP response
        response = MagicMock()
        response.raise_for_status.return_value = None
        self.table.requests.put = MagicMock(return_value=response)

        # Test method
        self.table.update_table(['New Value 1', 'New Value 2'])

        # Assertions
        self.mock_fetch_page_content.assert_called_once()
        self.table.requests.put.assert_called_once_with(
            f'{self.base_url}/rest/api/content/{self.page_id}',
            auth=(self.username, self.password),
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            json={
                "id": self.page_id,
                "type": "page",
                "title": "Test Page",
                "body": {
                    "storage": {
                        "value": "{table}\n|Header 1|Header 2|\n|Value 1|Value 2|\n|New Value 1|New Value 2|\n{table}",
                        "representation": "storage"
                    }
                },
                "version": {
                    "number": 3,
                    "minorEdit": True
                }
            }
        )

if __name__ == '__main__':
    unittest.main()

