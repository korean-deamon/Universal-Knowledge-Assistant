import os
import json
import requests
from langchain.tools import tool
from pydantic import BaseModel, Field
from src.config import GITHUB_TOKEN, GITHUB_REPO

class TicketSchema(BaseModel):
    name: str = Field(description="The name of the user creating the ticket")
    email: str = Field(description="The contact email of the user")
    summary: str = Field(description="A brief summary or title of the issue")
    description: str = Field(description="A detailed description of the problem")

@tool("create_support_ticket", args_schema=TicketSchema)
def create_support_ticket(name: str, email: str, summary: str, description: str) -> str:
    """
    Creates a support ticket in the issue tracking system (GitHub Issues). 
    Use this when a user needs further assistance or when information is not found in documents.
    """
    ticket_data = {
        "name": name,
        "email": email,
        "summary": summary,
        "description": description,
        "status": "Open"
    }
    
    # 1. Local Fallback (Always save locally for records)
    os.makedirs("tickets", exist_ok=True)
    ticket_id = len(os.listdir("tickets")) + 1
    file_path = f"tickets/ticket_{ticket_id}.json"
    with open(file_path, "w") as f:
        json.dump(ticket_data, f, indent=4)

    # 2. GitHub Integration
    github_status = ""
    if GITHUB_TOKEN:
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
            headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }
            payload = {
                "title": f"[TICKET #{ticket_id}] {summary}",
                "body": f"**User:** {name}\n**Email:** {email}\n\n**Description:**\n{description}"
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 201:
                issue_url = response.json().get("html_url")
                github_status = f" Also, a GitHub Issue has been created: {issue_url}"
            else:
                github_status = f" (GitHub sync failed: {response.status_code})"
        except Exception as e:
            github_status = f" (GitHub error: {str(e)})"
    else:
        github_status = " (Note: GitHub sync skipped - GITHUB_TOKEN not found in .env)"

    return f"Success! Ticket #{ticket_id} has been created for {name}.{github_status} Our team will contact you at {email} shortly."

# List of tools to be used by the AI Agent
tools = [create_support_ticket]
