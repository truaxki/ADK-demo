# ADK Tutorial - Progressive Weather Bot (ADK Tools Version)

This repository contains the code for the "Build Your First Intelligent Agent Team: A Progressive Weather Bot" tutorial, specifically structured for use with the Agent Development Kit (ADK) built-in command-line tools: `adk web`, `adk run`, and `adk api_server`.

This version allows you to run each step of the tutorial without manually setting up runners and session services, as those are handled by the ADK tools.

**Note:** If you prefer a notebook environment (like Colab or Jupyter) with manual control over runners and sessions, please refer to the [original notebook tutorial version](Your_Link_To_Notebook_Version_Here).

## Prerequisites

*   **Python:** Version 3.9 - 3.12 (Check ADK documentation for the latest compatibility).
*   **Git:** To clone this repository.
*   **LLM API Keys:** You will need API keys for the services used in the tutorial steps (Google Gemini, potentially OpenAI and Anthropic).
    *   Google AI Studio: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
    *   OpenAI Platform: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
    *   Anthropic Console: [https://console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
*   **OpenWeatherMap API Key:** Required for the enhanced weather functionality (free tier available).
    *   OpenWeatherMap: [https://home.openweathermap.org/api_keys](https://home.openweathermap.org/api_keys)
*   **SerpAPI Key:** Required for the web search functionality.
    *   SerpAPI: [https://serpapi.com/](https://serpapi.com/)

## Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/google/adk-docs.git
    cd adk-docs/examples/python/tutorial/agent_team/adk-tutorial/ # Navigate into the cloned directory
    ```

2.  **Create and Activate a Virtual Environment (Recommended):**
    This isolates project dependencies.

    *   **Create:**
        ```bash
        python -m venv .venv
        ```
    *   **Activate (execute in each new terminal session):**
        *   macOS / Linux:
            ```bash
            source .venv/bin/activate
            ```
        *   Windows (Command Prompt):
            ```bash
            .venv\Scripts\activate.bat
            ```
        *   Windows (PowerShell):
            ```ps1
            .venv\Scripts\Activate.ps1
            ```
        *(You should see `(.venv)` preceding your terminal prompt)*

3.  **Install Dependencies:**
    Install ADK and required packages.
    ```bash
    pip install google-adk
    pip install litellm
    pip install requests    # For weather API functionality
    pip install google-search-results  # For SerpAPI functionality
    ```

## Configuration: API Keys

Before running any agent step, you **must** configure your API keys.

1.  Navigate into the directory for the specific step you want to run (e.g., `step_1`, `step_2_anthropic`, `step_3`, etc.).
2.  Each step directory contains a `.env` file. Open this file in a text editor.
3.  Replace the placeholder values with your actual API keys.

    **Example `.env` content:**
    ```dotenv
    # Set to False to use API keys directly (required for multi-model)
    GOOGLE_GENAI_USE_VERTEXAI=FALSE

    # --- Replace with your actual keys ---
    GOOGLE_API_KEY=PASTE_YOUR_ACTUAL_GOOGLE_API_KEY_HERE
    ANTHROPIC_API_KEY=PASTE_YOUR_ACTUAL_ANTHROPIC_API_KEY_HERE
    OPENAI_API_KEY=PASTE_YOUR_ACTUAL_OPENAI_API_KEY_HERE
    OPENWEATHERMAP_API_KEY=PASTE_YOUR_ACTUAL_OPENWEATHERMAP_API_KEY_HERE
    SERPAPI_KEY=PASTE_YOUR_ACTUAL_SERPAPI_KEY_HERE
    # --- End of keys ---
    ```
4.  **Save the `.env` file.**
5.  **Repeat this process** for the `.env` file in *every* step directory you intend to run. The keys needed might vary slightly depending on the models used in that specific step.

## Running the Examples

Ensure your virtual environment is activated before running these commands.

### Using `adk web` (Recommended for Interactive UI)

1.  **Navigate to the parent `adk-tutorial` directory** (the one containing the `step_1`, `step_2_...` folders).
    ```bash
    # Make sure you are in the main 'adk-tutorial' folder
    cd /path/to/your/adk-tutorial
    ```
2.  **Run the command:**
    ```bash
    adk web
    ```
3.  This will start a local web server and likely open a new tab in your browser.
4.  In the web UI, you'll find a dropdown menu (usually on the left). Use this dropdown to **select the agent step** you want to interact with (e.g., `step_1`, `step_2_gpt4`, `step_6`).
5.  Once selected, you can type messages in the chat interface to interact with the agent for that specific step.

### Using `adk run` (Command-Line Interaction)

The `adk run` command allows you to interact with an agent directly from your terminal. You typically specify the path to the agent file.

*   **Example (running Step 1):**
    ```bash
    # Make sure you are in the main 'adk-tutorial' folder
    adk run step_1/agent.py
    ```
*   For detailed usage and options for `adk run`, please refer to the [Official ADK Documentation - Running Agents](https://google.github.io/adk-docs/get-started/running-agents/).

### Using `adk api_server` (Exposing as API)

The `adk api_server` command starts a FastAPI server, exposing your agent via an API endpoint.

*   **Example (serving Step 1):**
    ```bash
    # Make sure you are in the main 'adk-tutorial' folder
    adk api_server step_1/agent.py
    ```
*   For detailed usage, API endpoint structure, and options for `adk api_server`, please consult the [Official ADK Documentation - Running Agents](https://google.github.io/adk-docs/get-started/running-agents/).

## Current Project Structure

```
adk-tutorial/
├── coordinator_agent/
│   ├── utils/
│   │   ├── weather.py    # Enhanced weather functionality with geocoding support
│   │   └── search.py     # Web search functionality using SerpAPI
│   ├── agent.py          # Main coordinator agent
│   └── .env              # API Key configuration including OpenWeatherMap and SerpAPI
└── README.md             # This file
```

**Note:** The codebase has been streamlined to focus only on the coordinator agent with enhanced weather and search functionality. The step-by-step tutorial files are available in the original repository for reference.

## Enhanced Weather Functionality

The enhanced weather agent includes several improvements:

* **Real Weather Data**: Uses OpenWeatherMap API to provide actual weather conditions
* **Geocoding**: Converts city names to geographic coordinates using Nominatim (OpenStreetMap)
* **Temperature Unit Preferences**: Supports both Fahrenheit (default) and Celsius based on user preferences
* **Detailed Weather Reports**: Provides temperature, conditions, humidity, and wind speed
* **Error Handling**: Robust error handling for API failures and location lookup issues
* **In-Memory Caching**: Caches geocoding results to improve performance

To use this enhanced weather functionality:
1. Sign up for a free OpenWeatherMap API key
2. Add this key to the `.env` file as `OPENWEATHERMAP_API_KEY`
3. Interact with the agent asking for weather in any city (e.g., "What's the weather in Charleston, SC?")

## Guardrail Reference Code

The repository includes reference code for implementing guardrails in your agents. These guardrails can help ensure your agent:

* Properly validates and sanitizes user input
* Handles API errors gracefully
* Provides helpful fallback responses when services are unavailable
* Maintains context and state across conversation turns
* Respects user preferences for units and formatting

You can find examples of these guardrails implemented throughout the weather module code.

## Web Search Functionality

The agent includes web search capabilities using SerpAPI:

* **Real-time Information**: Access up-to-date information from the web
* **Structured Results**: Returns organized search results with snippets and URLs
* **Topic Research**: Can research topics beyond the agent's training data
* **Error Handling**: Gracefully handles API errors and rate limiting

To use the web search functionality:
1. Sign up for a SerpAPI key
2. Add this key to the `.env` file as `SERPAPI_KEY`
3. Interact with the agent asking for information (e.g., "What are the latest developments in AI?")