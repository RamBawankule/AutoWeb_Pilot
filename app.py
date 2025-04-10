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

# Initialize session state
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.getenv("GEMINI_API_KEY", "")
if 'browser_mode' not in st.session_state:
    st.session_state.browser_mode = "visible"
if 'model' not in st.session_state:
    st.session_state.model = "models/gemini-2.0-flash"
if 'setup_completed' not in st.session_state:
    st.session_state.setup_completed = False

class Post(BaseModel):
    caption: str
    url: str

class Posts(BaseModel):
    posts: List[Post]

controller = Controller(output_model=Posts)

def setup_components():
    st.title("Setup Configuration")
    
    # API Key input
    api_key = st.text_input(
        "Enter your Gemini API Key",
        value=st.session_state.api_key,
        type="password",
        help="Enter your Gemini API key to enable the search functionality"
    )
    
    # Model selection
    model = st.selectbox(
        "Select Model",
        options=[
            "models/gemini-2.5-pro-exp-03-25",
            "models/gemini-2.0-flash",
            "models/gemma-3-27b-it"
        ],
        index=1,
        help="Select the AI model to use for processing"
    )
    
    # Browser mode selection
    browser_mode = st.radio(
        "Select Browser Mode",
        options=["visible", "headless"],
        index=0 if st.session_state.browser_mode == "visible" else 1,
        help="Visible mode shows the browser window, headless mode runs in the background"
    )
    
    if st.button("Save Configuration"):
        if not api_key:
            st.error("Please enter your Gemini API key")
            return
        
        try:
            # Test API key by creating a simple chat instance
            ChatGoogleGenerativeAI(model=model, api_key=SecretStr(api_key))
            st.session_state.api_key = api_key
            st.session_state.browser_mode = browser_mode
            st.session_state.model = model
            st.session_state.setup_completed = True
            st.success("Configuration saved successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Invalid API key: {str(e)}")

def initialize_components():
    llm = ChatGoogleGenerativeAI(model=st.session_state.model, api_key=SecretStr(st.session_state.api_key))
    browser = Browser(config=BrowserConfig(headless=st.session_state.browser_mode == "headless"))
    return llm, browser

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

# Main application flow
if not st.session_state.setup_completed:
    setup_components()
else:
    # Initialize components with saved configuration
    llm, browser = initialize_components()
    
    st.title("AutoWeb Pilot")
    
    # Add a button to modify configuration
    if st.sidebar.button("Modify Configuration"):
        st.session_state.setup_completed = False
        st.rerun()
    
    search_query = st.text_input("Enter your search query:")
    if st.button("Run Search"):
        if search_query:
            with st.spinner("Processing..."):
                result = asyncio.run(run_agent(f"search '{search_query}' in google and give the first link from search results"))
                st.write(result)
        else:
            st.warning("Please enter a search query.")