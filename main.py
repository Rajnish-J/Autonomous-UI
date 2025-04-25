import asyncio
from Agent.anchor import create_anchor_session, close_anchor_session
from Agent.automation import run_automation
from Agent.logging import add_log, write_logs_to_file
from Agent.html_updater import update_html_with_session

async def main():
    print("🚀 Creating Anchor browser session...")
    add_log("🚀 Creating Anchor browser session...")

    # Create Anchor session
    session_id, cdp_url, live_view_url = create_anchor_session()

    print(f"🆔 Session ID: {session_id}")
    add_log(f"идентификатор сеанса: {session_id}")
    
    print(f"🔗 CDP URL: {cdp_url}")
    add_log(f"🔗 CDP URL: {cdp_url}")
    
    print(f"📺 Live View URL: {live_view_url}\n")
    add_log(f"📺 Live View URL: {live_view_url}\n")

    # Update HTML with session ID
    update_html_with_session(session_id)

    # Run automation task
    print("🤖 Running automation task...\n")
    add_log("🤖 Running automation task...\n")
    await run_automation(cdp_url)

    # Close Anchor session
    print("🛑 Closing the Anchor session...")
    add_log("🛑 Closing the Anchor session...")
    close_anchor_session(session_id)

    # Write logs to file
    write_logs_to_file()

if __name__ == "__main__":
    asyncio.run(main())