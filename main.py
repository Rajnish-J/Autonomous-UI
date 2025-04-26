import asyncio
from Agent.anchor import create_anchor_session, close_anchor_session
from Agent.automation import run_automation
from Agent.html_updater import update_html_with_session

async def main():
    # Create Anchor session
    session_id, cdp_url, live_view_url = create_anchor_session()

    # Update HTML with session ID
    update_html_with_session(session_id)

    # Run automation task
    await run_automation(cdp_url)

    # Close Anchor session
    close_anchor_session(session_id)

if __name__ == "__main__":
    asyncio.run(main())
    