# Multi-Agent System with Voice Support

This project demonstrates a multi-agent system built with Google's Agent Development Kit (ADK) that supports voice-to-voice interactions and uses real APIs.

## Features

- **Coordinator Agent**: Routes requests to specialized sub-agents
- **Real Weather API**: Get current weather information using OpenWeatherMap API
- **SERPAPI Web Search**: Search the web using SERPAPI
- **Weather Information**: Get weather reports with temperature unit conversion
- **Greeting & Farewell**: Handle conversation openings and closings
- **Voice-to-Voice**: Support for natural spoken conversations
- **Proper Delegation**: Coordinator correctly delegates to specialized sub-agents using the '@agent_name' format

## Prerequisites

- Python 3.11+
- ADK Tools (`pip install adktools`)
- API Keys (see below)

## API Keys Setup

### OpenWeatherMap API (for weather data)
1. Create a free account at [OpenWeatherMap](https://home.openweathermap.org/users/sign_up)
2. Navigate to your [API keys](https://home.openweathermap.org/api_keys) page
3. Create a new API key or use your existing one
4. Set it as an environment variable:
   ```
   # Windows
   set OPENWEATHERMAP_API_KEY=your_api_key_here
   
   # macOS/Linux
   export OPENWEATHERMAP_API_KEY=your_api_key_here
   ```

### SERPAPI (for web search)
1. Create an account at [SERPAPI](https://serpapi.com/users/sign_up)
2. Get your API key from the dashboard
3. Set it as an environment variable:
   ```
   # Windows
   set SERPAPI_KEY=your_api_key_here
   
   # macOS/Linux
   export SERPAPI_KEY=your_api_key_here
   ```

## Installation

1. Make sure you have installed the dependencies:
   ```
   pip install -e .
   ```

2. Set your API keys as environment variables (see above)

## Running the Agent with Voice Support

To run the agent with voice support:

1. Start the ADK web interface:
   ```
   adk web
   ```

2. Open the provided URL in your web browser (typically http://localhost:8080)

3. Use the microphone button in the web interface to speak to the agent

4. The agent will respond with both text and voice

## Voice-to-Voice Implementation Details

The ADK web interface provides built-in support for:
- Speech recognition (voice-to-text)
- Agent processing
- Text-to-speech (text-to-voice)

This is all handled automatically by the ADK web interface when you use `adk web`.

## Agent Structure

The system consists of:
- **Reasoning Agnet**: Runs o3 mini reasoning model
- **Coordinator Agent**: Main entry point that delegates to specialized agents
- **Weather Agent**: Handles weather queries and unit preferences using real OpenWeatherMap data
- **Greeting Agent**: Processes greetings and salutations
- **Farewell Agent**: Manages conversation closings

## Custom Tools

- `search_web`: Searches the web using SERPAPI
- `get_weather_stateful`: Provides real-time weather information from OpenWeatherMap API
- `set_temperature_unit`: Updates user preferences for temperature units
- `say_hello`: Generates greetings
- `say_goodbye`: Creates farewell messages

## Project Structure

The code is organized in a modular way:
- `agent.py` - Main coordinator agent definition and sub-agents
- `utils/` - Modular utility functions:
  - `weather.py` - OpenWeatherMap API integration
  - `search.py` - Web search functionality
  - `preferences.py` - User preference management
  - `conversation.py` - Greeting and farewell handlers

## Troubleshooting

If you encounter an error like `Function weather_agent is not found in the tools_dict`, make sure the coordinator agent is properly delegating to sub-agents using the '@agent_name' format instead of trying to call functions directly. This error occurs when the LLM tries to call a tool with the same name as a sub-agent instead of delegating to that sub-agent.

## License

Apache License 2.0 