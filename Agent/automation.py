from browser_use import BrowserConfig
from browser_use import Browser

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
load_dotenv()

import asyncio

config = BrowserConfig(
    cdp_url=f"wss://connect.anchorbrowser.io?apiKey=sk-0552929166f6b70537925ced9b7a6c94&sessionId=57c06915-b54e-4932-9c57-8e4a58c4d716"
)
# llm = ChatOpenAI(model="gpt-4o")
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp')

browser = Browser(config=config)

async def main():
    agent = Agent(
        browser=browser,
        task="As a user I want to navigate to https://google.com and search for ai toolsAs a user I want to navigate to https://google.com and search for ai tools",
        llm=llm,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())