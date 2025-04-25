import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use.browser.context import BrowserContextConfig
import os
from pydantic import SecretStr

from browser_use import Agent, Browser
from browser_use.browser.context import BrowserContext

def __init__(self, model_name='gemini-2.0-flash-exp'):
        self.llm = ChatGoogleGenerativeAI(model=model_name, api_key=get_api_key())

def get_api_key():
    return SecretStr(os.getenv("GEMINI_API_KEY"))

# Reuse existing browser
browser = Browser()
config = BrowserContextConfig(
    cookies_file="path/to/cookies.json",
    wait_for_network_idle_page_load_time=3.0,
    browser_window_size={'width': 1280, 'height': 1100},
    locale='en-US',
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    highlight_elements=True,
    viewport_expansion=500,
    allowed_domains=['google.com', 'wikipedia.org'],
)
context = BrowserContext(browser=browser, config=config)
agent = Agent(
    task=task1,
    llm=llm,
    browser=browser  # Browser instance will be reused
)

await agent.run()
