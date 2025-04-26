import os
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import BrowserConfig, Browser, Agent

async def run_automation(cdp_url):
    google_api_key = os.getenv("GOOGLE_API_KEY")
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=google_api_key)

    config = BrowserConfig(cdp_url=cdp_url)
    browser = Browser(config=config)

    agent = Agent(
        browser=browser,
        task="As a user I want to navigate to https://google.com and search for ai tools",
        llm=llm,
    )

    result = await agent.run()
    return result
