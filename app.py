import sys
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser, BrowserConfig, Controller
from pydantic import SecretStr, BaseModel
from typing import List
import os
from dotenv import load_dotenv
import asyncio

import subprocess
subprocess.run(["playwright", "install"], check=True)

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
    try:
        llm = ChatGoogleGenerativeAI(model=st.session_state.model, api_key=SecretStr(st.session_state.api_key))
        browser_config = BrowserConfig(headless=st.session_state.browser_mode == "headless")
        browser = Browser(config=browser_config)
        return llm, browser
    except Exception as e:
        st.error(f"Failed to initialize components: {str(e)}")
        raise

async def run_agent(task: str):
    browser = None
    try:
        # Initialize browser with Playwright configuration
        browser_config = BrowserConfig(
            headless=st.session_state.browser_mode == "headless",
            playwright_args=[
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-gpu"
            ]
        )
        browser = Browser(config=browser_config)
        
        agent = Agent(
            task=task,
            llm=llm,
            browser=browser,
            controller=controller
        )
        result = await agent.run()
        final_result = result.final_result()
        
        if final_result is None:
            st.error("No result was returned from the agent")
            return "No result found."
            
        if isinstance(final_result, dict) and 'posts' in final_result:
            # Handle Posts model output
            posts = final_result['posts']
            if posts and len(posts) > 0:
                return format_output(posts[0])
        
        formatted_result = format_output(final_result)
        return formatted_result
    except Exception as e:
        st.error(f"Browser error: {type(e).__name__}: {str(e)}")
        if browser:
            try:
                await browser.close()
            except Exception as close_error:
                st.warning(f"Failed to close browser: {str(close_error)}")
            browser = None
        return f"Error: {str(e)}"
    finally:
        if browser:
            try:
                await browser.close()
                browser = None
            except Exception as e:
                st.warning(f"Error during final browser cleanup: {str(e)}")
                browser = None

def format_output(result):
    try:
        # Handle Posts model output
        if isinstance(result, dict):
            if 'posts' in result and result['posts'] and len(result['posts']) > 0:
                post = result['posts'][0]
                return f"Caption: {post.get('caption', 'N/A')}, URL: {post.get('url', 'N/A')}"
            return f"Caption: {result.get('caption', 'N/A')}, URL: {result.get('url', 'N/A')}"
        
        # Handle string output
        if isinstance(result, str):
            if ',' in result:
                parts = result.split(',')
                caption = parts[0].strip()
                url = parts[1].strip() if len(parts) > 1 else 'N/A'
                return f"Caption: {caption}, URL: {url}"
            return f"Result: {result}"
            
        # Handle other types
        return str(result)
    except Exception as e:
        st.warning(f"Error formatting output: {str(e)}")
        return str(result)

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
