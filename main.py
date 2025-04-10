from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from pydantic import SecretStr
import os
from dotenv import load_dotenv
import sys
load_dotenv()

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
import asyncio
from browser_use import Agent, Browser, BrowserConfig, Controller
from langchain_openai import ChatOpenAI
import asyncio
from pydantic import BaseModel
from typing import List

class Post(BaseModel):
    caption: str
    url: str
class Posts(BaseModel):
    posts: List[Post]

controller = Controller(output_model=Posts)


api_key = os.getenv("GEMINI_API_KEY")

# Initialize the model
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=SecretStr(os.getenv('GEMINI_API_KEY')))


# Configure the browser
browser = Browser(
    config=BrowserConfig(
        headless=True
    )
)

async def main():
    # Change the encoding to utf-8
    sys.stdout.reconfigure(encoding='utf-8')
    
    agent = Agent(
        task="search 'ram bawankule' in google and give the first link from search results",
        llm=llm,
        browser=browser,
        controller=controller
    )
    result = await agent.run()
    print(result.final_result())
    await browser.close()

if __name__ == '__main__':
    import asyncio
    
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())