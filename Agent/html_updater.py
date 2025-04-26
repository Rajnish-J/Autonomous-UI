import os
import re

def update_html_with_session(session_id):
    html_path = os.path.join(os.path.dirname(__file__), "..", "index.html")

    with open(html_path, "r") as file:
        html_content = file.read()

    updated_html = re.sub(
        r"(https://live\.anchorbrowser\.io\?sessionId=)[^\"']+",
        f"https://live.anchorbrowser.io?sessionId={session_id}",
        html_content
    )

    with open(html_path, "w") as file:
        file.write(updated_html)
