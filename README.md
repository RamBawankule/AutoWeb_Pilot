# Browser Automation with Gemini AI

This project is a web application that combines browser automation with Google's Gemini AI to perform automated web searches and return structured results. Built with Streamlit, it provides a user-friendly interface for interacting with the automated browser.

## Features

- Web-based interface using Streamlit
- Integration with Google Gemini AI for intelligent automation
- Automated browser control for web searches
- Structured output formatting
- Asynchronous operation support

## Prerequisites

- Python 3.x
- A Google Gemini AI API key

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the project root
2. Add your Gemini AI API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

### Running the Web Interface

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```
2. Open your browser and navigate to the provided URL (typically http://localhost:8501)
3. Enter your search query in the text input
4. Click "Run Search" to execute the automated search

### Running from Command Line

Alternatively, you can run the automation script directly:

```bash
python main.py
```

## Project Structure

- `app.py`: Streamlit web interface
- `main.py`: Command-line interface and core functionality
- `requirements.txt`: Project dependencies
- `.env`: Environment variables configuration

## Output Format

The application returns search results in a structured format containing:
- Caption: Description or title of the search result
- URL: The corresponding web link

## Notes

- The browser automation is configured to run in visible mode by default in the web interface
- The command-line version runs in headless mode
- Windows users: The application automatically configures the correct event loop policy for asyncio operations