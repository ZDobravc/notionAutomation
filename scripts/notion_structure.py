from notion_client import Client
import os
from dotenv import load_dotenv

def find_or_create_child_page(notion: Client, parent_id: str, title: str) -> str:
    print(f"\nLooking for page titled '{title}' under parent: {parent_id}")

    # List all child blocks of the parent page
    children = notion.blocks.children.list(parent_id)["results"]
    print(f"Found {len(children)} children under parent.")

    # Look for a child page with the given title
    for block in children:
        if block["type"] == "child_page":
            block_title = block["child_page"]["title"]
            print(f" - Existing child page: {block_title}")
            if block_title == title:
                print(f"   -> Match found. Using existing page ID: {block['id']}")
                return block["id"]

    # If not found, create a new child page
    print(f"No match found. Creating new page titled '{title}' under parent: {parent_id}")
    response = notion.pages.create(
        parent={"page_id": parent_id},
        properties={
            "title": [
                {
                    "type": "text",
                    "text": {
                        "content": title
                    }
                }
            ]
        }
    )
    print(f"   -> Created new page. ID: {response['id']}")
    return response["id"]

def ensure_year_and_month_pages(notion: Client, root_page_id: str, year: int, month: str):
    print(f"\nEnsuring pages for year '{year}' and month '{month}' exist under root: {root_page_id}")
    year_page_id = find_or_create_child_page(notion, root_page_id, str(year))
    month_page_id = find_or_create_child_page(notion, year_page_id, month)
    print(f"Confirmed structure: {year} → {month}")
    return year_page_id, month_page_id


if __name__ == "__main__":
    from datetime import date
    load_dotenv()

    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    root_page_id = os.getenv("NOTES_PARENT_PAGE_ID")

    today = date.today()
    year = today.year
    month = today.strftime("%B")  # e.g., "April"

    print("\n--- Running standalone page structure check ---")
    year_page_id, month_page_id = ensure_year_and_month_pages(notion, root_page_id, year, month)
    print(f"\nYear Page ID: {year_page_id}")
    print(f"Month Page ID: {month_page_id}")
