import os
import re
import requests
import asyncio
from dotenv import load_dotenv

from browser_use import BrowserConfig, Browser, Agent
from langchain_google_genai import ChatGoogleGenerativeAI

# Load .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Get API keys
google_api_key = os.getenv("GOOGLE_API_KEY")
anchor_api_key = os.getenv("ANCHOR_API_KEY")

# List to collect logs
execution_logs = []

# Define the log file path
def get_log_file_path():
    agent_folder = os.path.dirname(__file__)
    log_file_path = os.path.join(agent_folder, "execution_logs.txt")
    return log_file_path

# Add a log message to the execution_logs list
def add_log(log_message):
    execution_logs.append(log_message)

# Write all collected logs to a text file
def write_logs_to_file():
    log_file_path = get_log_file_path()
    try:
        # Open the file in append mode to ensure logs are added at the end
        with open(log_file_path, "a") as log_file:  # Use "a" to append
            log_file.write("\n".join(execution_logs) + "\n")
        print("✅ Logs appended to execution_logs.txt.")
    except Exception as e:
        print(f"❌ Failed to write to log file: {str(e)}")


# 🔁 Update the HTML iframe with the latest sessionId
def update_html_with_session(session_id):
    html_path = os.path.join(os.path.dirname(__file__), '..', 'index.html')

    try:
        with open(html_path, "r") as file:
            html_content = file.read()

        updated_html = re.sub(
            r"(https://live\.anchorbrowser\.io\?sessionId=)[^\"']+",
            f"https://live.anchorbrowser.io?sessionId={session_id}",
            html_content
        )

        with open(html_path, "w") as file:
            file.write(updated_html)

        print("✅ index.html updated with new sessionId.")
        add_log(f"✅ index.html updated with new sessionId: {session_id}")
    except Exception as e:
        print("❌ Failed to update HTML file:", str(e))
        add_log(f"❌ Failed to update HTML file: {str(e)}")

# Create Anchor browser session
def create_anchor_session():
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

    try:
        response_json = response.json()
        print("📦 Full API Response:", response_json)
        add_log(f"📦 Full API Response: {response_json}")

        if "data" not in response_json:
            raise ValueError(f"Anchor API Error: {response_json.get('message', 'Unknown error')}")

        data = response_json["data"]
        return data["id"], data["cdp_url"], data["live_view_url"]

    except Exception as e:
        print("❌ Error creating Anchor session:", str(e))
        add_log(f"❌ Error creating Anchor session: {str(e)}")
        raise

# Close the Anchor browser session
def close_anchor_session(session_id):
    response = requests.delete(
        f"https://api.anchorbrowser.io/v1/sessions/{session_id}",
        headers={
            "anchor-api-key": anchor_api_key,
            "Content-Type": "application/json",
        }
    )

    try:
        response_json = response.json()
        if response.status_code == 200:
            print(f"✅ Successfully closed session: {session_id}")
            add_log(f"✅ Successfully closed session: {session_id}")
        else:
            print(f"❌ Failed to close session: {session_id}")
            add_log(f"❌ Failed to close session: {session_id}")
    except Exception as e:
        print("❌ Error closing Anchor session:", str(e))
        add_log(f"❌ Error closing Anchor session: {str(e)}")

# Run browser automation
async def run_automation(cdp_url):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=google_api_key)

    config = BrowserConfig(cdp_url=cdp_url)
    browser = Browser(config=config)

    agent = Agent(
        browser=browser,
        task="As a user I want to navigate to https://google.com and search for ai tools",
        llm=llm,
    )

    result = await agent.run()
    print("\n✅ Automation Task Result:\n", result)
    add_log(f"✅ Automation Task Result: {result}")

# Main function
async def main():
    print("🚀 Creating Anchor browser session...")
    add_log("🚀 Creating Anchor browser session...")

    session_id, cdp_url, live_view_url = create_anchor_session()

    print(f"🆔 Session ID: {session_id}")
    add_log(f"🆔 Session ID: {session_id}")
    
    print(f"🔗 CDP URL: {cdp_url}")
    add_log(f"🔗 CDP URL: {cdp_url}")
    
    print(f"📺 Live View URL: {live_view_url}\n")
    add_log(f"📺 Live View URL: {live_view_url}\n")

    update_html_with_session(session_id)

    print("🤖 Running automation task...\n")
    add_log("🤖 Running automation task...\n")
    await run_automation(cdp_url)

    print("🛑 Closing the Anchor session...")
    add_log("🛑 Closing the Anchor session...")
    close_anchor_session(session_id)

    # After all tasks are done, write the logs to a file
    write_logs_to_file()

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
