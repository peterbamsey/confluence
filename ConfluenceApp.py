import argparse
from confluence_table import ConfluenceTable

def main():
    parser = argparse.ArgumentParser(description='Update a Confluence page table')
    parser.add_argument('--username', required=True, help='Confluence username')
    parser.add_argument('--password', required=True, help='Confluence password')
    parser.add_argument('--base-url', required=True, help='Confluence base URL')
    parser.add_argument('--page-id', required=True, help='Confluence page ID')
    parser.add_argument('--new-row', nargs='+', required=True, help='New row to add to the table')

    args = parser.parse_args()

    table = ConfluenceTable(args.username, args.password, args.base_url, args.page_id)
    table.update_table(args.new_row)

if __name__ == '__main__':
    main()

