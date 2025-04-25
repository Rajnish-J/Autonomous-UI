import os
import requests
from dotenv import load_dotenv
from Agent.logging import add_log

# Load .env file
load_dotenv()

# Get API key
anchor_api_key = os.getenv("ANCHOR_API_KEY")

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
        add_log(f"📦 Full API Response: {response_json}")

        if "data" not in response_json:
            raise ValueError(f"Anchor API Error: {response_json.get('message', 'Unknown error')}")

        data = response_json["data"]
        return data["id"], data["cdp_url"], data["live_view_url"]

    except Exception as e:
        add_log(f"❌ Error creating Anchor session: {str(e)}")
        raise

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
            add_log(f"✅ Successfully closed session: {session_id}")
        else:
            add_log(f"❌ Failed to close session: {session_id}")
    except Exception as e:
        add_log(f"❌ Error closing Anchor session: {str(e)}")