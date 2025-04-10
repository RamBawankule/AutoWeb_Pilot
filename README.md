# Browser Automation with Gemini AI

This project is a web application that combines browser automation with Google's Gemini AI to perform automated web searches and return structured results. Built with Streamlit, it provides a user-friendly interface for interacting with the automated browser.

## Features

- Web-based interface using Streamlit
- Integration with Google Gemini AI for intelligent automation
- Multiple AI model options (Gemini 2.5 Pro, Gemini 2.0 Flash, Gemma 3 27B)
- Configurable browser modes (visible/headless)
- Automated browser control for web searches
- Structured output formatting
- Asynchronous operation support

## Prerequisites

- Python 3.x
- A Google Gemini AI API key
- Modern web browser (Chrome recommended)

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

### Model Selection

The application supports multiple AI models:
- `models/gemini-2.5-pro-exp-03-25`: Latest Gemini Pro model with enhanced capabilities
- `models/gemini-2.0-flash`: Optimized for faster response times
- `models/gemma-3-27b-it`: Alternative model option

### Browser Modes

- **Visible Mode**: Shows the browser window during automation
  - Useful for debugging and understanding the automation process
  - Default mode in the web interface
- **Headless Mode**: Runs browser in the background
  - More efficient for production use
  - Default mode in command-line interface

## Usage

### Running the Web Interface

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```
2. Open your browser and navigate to the provided URL (typically http://localhost:8501)
3. Configure your settings:
   - Enter your Gemini API key
   - Select your preferred AI model
   - Choose browser mode (visible/headless)
4. Enter your search query in the text input
5. Click "Run Search" to execute the automated search

### Running from Command Line

Alternatively, you can run the automation script directly:

```bash
python main.py
```

## Project Structure

- `app.py`: Streamlit web interface and application logic
- `main.py`: Command-line interface and core functionality
- `requirements.txt`: Project dependencies
- `.env`: Environment variables configuration

## Output Format

The application returns search results in a structured format containing:
- Caption: Description or title of the search result
- URL: The corresponding web link

## Troubleshooting

### Common Issues

1. **API Key Issues**
   - Ensure your Gemini API key is valid and properly set in the `.env` file
   - Check that the API key has the necessary permissions

2. **Browser Automation Issues**
   - Make sure you have a compatible browser installed
   - Try switching between visible and headless modes
   - Check your internet connection

3. **Event Loop Errors (Windows)**
   - The application automatically configures the correct event loop policy
   - If you encounter issues, try restarting the application

## Notes

- The browser automation is configured to run in visible mode by default in the web interface
- The command-line version runs in headless mode
- Windows users: The application automatically configures the correct event loop policy for asyncio operations
- For best results, ensure a stable internet connection and keep your browser updated