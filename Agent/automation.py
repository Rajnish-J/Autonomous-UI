import os
import asyncio
from dotenv import load_dotenv

from browser_use import BrowserConfig, Browser, Agent
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize LLM with your Gemini API key
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', google_api_key=google_api_key)

# Configure the browser session
config = BrowserConfig(
    cdp_url="wss://connect.anchorbrowser.io?apiKey=sk-0552929166f6b70537925ced9b7a6c94&sessionId=f3cbfdc4-af04-45cd-80e7-cea72043ff57"
)

browser = Browser(config=config)

async def main():
    agent = Agent(
        browser=browser,
        task="As a user I want to navigate to https://google.com and search for ai tools",
        llm=llm,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
