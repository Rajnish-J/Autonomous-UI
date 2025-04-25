import os
import re
from Agent.logging import add_log

def update_html_with_session(session_id):
    html_path = os.path.join(os.path.dirname(__file__), "..", "index.html")

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