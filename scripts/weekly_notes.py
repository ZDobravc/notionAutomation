import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))

weekly_notes_id = os.getenv("WEEKLY_NOTES_PAGE_ID")

def get_weekly_notes_content(page_id):
    children = notion.blocks.children.list(page_id)["results"]
    content = []

    for block in children:
        if block["type"] == "paragraph":
            text = block["paragraph"]["rich_text"]
            line = "".join([t["plain_text"] for t in text])
            content.append(line)

    return "\n".join(content)

if __name__ == "__main__":
    text = get_weekly_notes_content(weekly_notes_id)
    print("📝 Weekly Notes Content:\n")
    print(text)
