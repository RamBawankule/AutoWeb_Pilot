import sys
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser, BrowserConfig, Controller
from pydantic import SecretStr, BaseModel
from typing import List
import os
from dotenv import load_dotenv
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

load_dotenv()

class Post(BaseModel):
    caption: str
    url: str

class Posts(BaseModel):
    posts: List[Post]

controller = Controller(output_model=Posts)
api_key = os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=SecretStr(api_key))
browser = Browser(config=BrowserConfig(headless=False))

async def run_agent(task: str):
    agent = Agent(
        task=task,
        llm=llm,
        browser=browser,
        controller=controller
    )
    result = await agent.run()
    await browser.close()
    final_result = result.final_result()
    if final_result is None:
        return "No result found."
    formatted_result = format_output(final_result)
    return formatted_result

def format_output(result):
    # Check if result is a string and format accordingly
    if isinstance(result, str):
        # Assuming the result is a simple string with caption and URL separated by a comma
        parts = result.split(',')
        caption = parts[0].strip() if len(parts) > 0 else 'N/A'
        url = parts[1].strip() if len(parts) > 1 else 'N/A'
        formatted_result = f"Caption: {caption}, URL: {url}"
    else:
        # Assuming result is a dictionary or similar structure
        formatted_result = f"Caption: {result.get('caption', 'N/A')}, URL: {result.get('url', 'N/A')}"
    return formatted_result

st.title("Browser Automation with Gemini")
search_query = st.text_input("Enter your search query:")
if st.button("Run Search"):
    if search_query:
        with st.spinner("Processing..."):
            result = asyncio.run(run_agent(f"search '{search_query}' in google and give the first link from search results"))
            st.write(result)
    else:
        st.warning("Please enter a search query.")