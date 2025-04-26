import os
import requests
from dotenv import load_dotenv

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

    response_json = response.json()
    if "data" not in response_json:
        raise ValueError(f"Anchor API Error: {response_json.get('message', 'Unknown error')}")

    data = response_json["data"]
    return data["id"], data["cdp_url"], data["live_view_url"]

def close_anchor_session(session_id):
    requests.delete(
        f"https://api.anchorbrowser.io/v1/sessions/{session_id}",
        headers={
            "anchor-api-key": anchor_api_key,
            "Content-Type": "application/json",
        }
    )
