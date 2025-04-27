import asyncio
import os
import re
import requests
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import BrowserConfig, Browser, Agent
from sqlalchemy.orm import Session

# Import database modules
from database import engine, SessionLocal, Base
import models
import repository

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Load .env file
load_dotenv()

# Get API keys
anchor_api_key = os.getenv("ANCHOR_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

def create_anchor_session():
    """Create an Anchor session and return session ID, CDP URL, and live view URL."""
    response = requests.post(
        "https://api.anchorbrowser.io/v1/sessions",
        headers={
            "anchor-api-key": anchor_api_key,
            "Content-Type": "application/json",
        },
        json={
            "browser": {
                "headless": {"active": False}
            }
        }
    )

    response_json = response.json()
    if "data" not in response_json:
        raise ValueError(f"Anchor API Error: {response_json.get('message', 'Unknown error')}")

    data = response_json["data"]
    return data["id"], data["cdp_url"], data["live_view_url"]

def close_anchor_session(session_id):
    """Close an Anchor session by session ID."""
    requests.delete(
        f"https://api.anchorbrowser.io/v1/sessions/{session_id}",
        headers={
            "anchor-api-key": anchor_api_key,
            "Content-Type": "application/json",
        }
    )

def update_html_with_session(session_id):
    """Update the HTML file with the new session ID."""
    # Get the directory of the current script (main.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to index.html
    html_path = os.path.join(current_dir, "index.html")

    with open(html_path, "r") as file:
        html_content = file.read()

    updated_html = re.sub(
        r"(https://live\.anchorbrowser\.io\?sessionId=)[^\"']+",
        f"https://live.anchorbrowser.io?sessionId={session_id}",
        html_content
    )

    with open(html_path, "w") as file:
        file.write(updated_html)

async def run_automation(cdp_url, task_description, db_task_id):
    """Run automation using LangChain and Google Generative AI."""
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=google_api_key)

    config = BrowserConfig(cdp_url=cdp_url)
    browser = Browser(config=config)

    agent = Agent(
        browser=browser,
        task=task_description,
        llm=llm,
    )

    try:
        result = await agent.run()
        # Update task result in the database
        with SessionLocal() as db:
            repository.update_task_result(db, db_task_id, result)
        return result
    except Exception as e:
        # Update task status to failed in the database
        with SessionLocal() as db:
            repository.update_task_result(db, db_task_id, {"error": str(e)}, status="failed")
        raise

async def main():
    """Main function to orchestrate the workflow."""
    db_session = None
    session_id = None
    
    try:
        # Create Anchor session
        session_id, cdp_url, live_view_url = create_anchor_session()
        print(f"Session created. Live View URL: {live_view_url}")

        # Store session in database
        with SessionLocal() as db:
            db_session = repository.create_session(db, session_id, cdp_url, live_view_url)
        
        # Update HTML with session ID
        update_html_with_session(session_id)
        print("HTML file updated with session ID.")

        # Define the task
        task_description = "As a user I want to navigate to https://google.com and search for ai tools"
        
        # Create task in database
        with SessionLocal() as db:
            db_task = repository.create_task(db, session_id, task_description)
            task_id = db_task.id
        
        # Run automation task
        print("Starting automation task...")
        result = await run_automation(cdp_url, task_description, task_id)
        print(f"Automation completed. Result: {result}")

    finally:
        # Ensure the session is closed even if an error occurs
        if session_id:
            close_anchor_session(session_id)
            # Mark session as closed in database
            with SessionLocal() as db:
                repository.close_session(db, session_id)
            print("Anchor session closed.")

if __name__ == "__main__":
    asyncio.run(main())