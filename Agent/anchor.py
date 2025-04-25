import requests

# ANCHOR_API_KEY = "YOUR_ANCHOR_API_KEY"

response = requests.post(
    "https://api.anchorbrowser.io/v1/sessions",
    headers={
        "anchor-api-key": "sk-0552929166f6b70537925ced9b7a6c94",
        "Content-Type": "application/json",
    },
    json={
      "browser": {
        "headless": {"active": False} 
      }
    }).json()

session_data = response["data"]
print(session_data)