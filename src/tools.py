import os
import json
from langchain.tools import tool
from pydantic import BaseModel, Field

class TicketSchema(BaseModel):
    name: str = Field(description="The name of the user creating the ticket")
    email: str = Field(description="The contact email of the user")
    summary: str = Field(description="A brief summary or title of the issue")
    description: str = Field(description="A detailed description of the problem")

@tool("create_support_ticket", args_schema=TicketSchema)
def create_support_ticket(name: str, email: str, summary: str, description: str) -> str:
    """
    Creates a support ticket in the issue tracking system. 
    Use this when a user needs further assistance or when information is not found in documents.
    """
    # In a real-world scenario, you would call the GitHub or Jira API here.
    # For now, we will simulate this by saving to a local JSON file.
    
    ticket_data = {
        "name": name,
        "email": email,
        "summary": summary,
        "description": description,
        "status": "Open",
        "priority": "Normal"
    }
    
    # Ensure tickets directory exists
    os.makedirs("tickets", exist_ok=True)
    
    ticket_id = len(os.listdir("tickets")) + 1
    file_path = f"tickets/ticket_{ticket_id}.json"
    
    with open(file_path, "w") as f:
        json.dump(ticket_data, f, indent=4)
    
    return f"Success! Ticket #{ticket_id} has been created for {name}. Our team will contact you at {email}."

# List of tools to be used by the AI Agent
tools = [create_support_ticket]
