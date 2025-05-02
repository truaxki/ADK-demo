# Weather & Search Agent Tutorial

A simple demonstration agent built with the Agent Development Kit (ADK) that can provide weather information and web search results.

## Required API Keys

* **LLM API Key:** Google Gemini, OpenAI, or Anthropic (choose one based on your preference)
* **OpenWeatherMap API Key:** For weather data - [Get key here](https://home.openweathermap.org/api_keys)
* **SerpAPI Key:** For web search functionality - [Get key here](https://serpapi.com/)

## Quick Setup

1. **Install dependencies:**
   ```bash
   pip install google-adk litellm requests google-search-results
   ```

2. **Set up your `.env` file in the coordinator_agent directory:**
   ```
   GOOGLE_API_KEY=your_google_key_here
   # Or alternatively:
   # OPENAI_API_KEY=your_openai_key_here
   # ANTHROPIC_API_KEY=your_anthropic_key_here
   
   OPENWEATHERMAP_API_KEY=your_openweathermap_key_here
   SERPAPI_KEY=your_serpapi_key_here
   ```

3. **Run the agent:**
   ```bash
   adk run coordinator_agent/agent.py
   # Or for web interface:
   adk web
   ```

## Features

* **Weather Information:** Get current weather conditions for any city
* **Web Search:** Find up-to-date information from the internet
* **Smart Conversation:** Maintains context across multiple turns

## Project Structure

```
coordinator_agent/
├── utils/
│   ├── weather.py    # Weather functionality
│   └── search.py     # Web search functionality
├── agent.py          # Main agent logic
└── .env              # Your API keys (create this file)
```

## Example Interactions

* "What's the weather in New York?"
* "I prefer temperatures in Celsius"
* "What are the latest developments in AI?"
* "Search for healthy dinner recipes"