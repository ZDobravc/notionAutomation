import os
import smtplib
from datetime import date
from dotenv import load_dotenv
from notion_client import Client
from email.mime.text import MIMEText

from scripts.date_builder import format_week_range
from scripts.notion_structure import ensure_year_and_month_pages

load_dotenv()
notion = Client(auth=os.getenv("NOTION_TOKEN"))

weekly_notes_id = os.getenv("WEEKLY_NOTES_PAGE_ID")
root_page_id = os.getenv("NOTES_PARENT_PAGE_ID")

def get_weekly_notes_content(page_id):
    children = notion.blocks.children.list(page_id)["results"]
    content = []

    for block in children:
        if block["type"] == "paragraph":
            text = block["paragraph"]["rich_text"]
            line = "".join([t["plain_text"] for t in text])
            content.append(line)

    return "\n".join(content)

def create_weekly_page(notion: Client, parent_id: str, title: str) -> str:
    response = notion.pages.create(
        parent={"page_id": parent_id},
        properties={
            "title": [
                {
                    "type": "text",
                    "text": {"content": title}
                }
            ]
        }
    )
    return response["id"]

def insert_text_blocks(notion: Client, page_id: str, content: str):
    lines = content.splitlines()
    blocks = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": line}}]
            }
        }
        for line in lines
    ]

    if blocks:
        notion.blocks.children.append(page_id, children=blocks)

def clear_page_content(notion: Client, page_id: str):
    children = notion.blocks.children.list(page_id)["results"]
    for block in children:
        block_id = block["id"]
        notion.blocks.delete(block_id)

def send_email(subject: str, body: str, to_email: str):
    from_email = os.getenv("GMAIL_USER")
    app_password = os.getenv("GMAIL_APP_PASSWORD")

    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(from_email, app_password)
        server.send_message(msg)

if __name__ == "__main__":
    today = date.today()
    week_label = format_week_range(today)

    year = today.year
    month = today.strftime("%B")
    year_page_id, month_page_id = ensure_year_and_month_pages(notion, root_page_id, year, month)

    text = get_weekly_notes_content(weekly_notes_id)
    new_page_id = create_weekly_page(notion, month_page_id, week_label)
    insert_text_blocks(notion, new_page_id, text)
    clear_page_content(notion, weekly_notes_id)

    recipient = os.getenv("RECIPIENT_EMAIL")
    email_subject = f"Weekly Notes ({week_label})"
    send_email(email_subject, text, recipient)
