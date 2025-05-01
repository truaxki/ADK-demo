# Multi-Agent System with Voice Support

This project demonstrates a multi-agent system built with Google's Agent Development Kit (ADK) that supports voice-to-voice interactions.

## Features

- **Coordinator Agent**: Routes requests to specialized sub-agents
- **SERPAPI Web Search**: Search the web using SERPAPI
- **Weather Information**: Get weather reports with temperature unit conversion
- **Greeting & Farewell**: Handle conversation openings and closings
- **Voice-to-Voice**: Support for natural spoken conversations

## Prerequisites

- Python 3.11+
- ADK Tools (`pip install adktools`)
- SERPAPI API Key (set as environment variable)

## Installation

1. Make sure you have installed the dependencies:
   ```
   pip install -e .
   ```

2. Set your SERPAPI API key as an environment variable:
   ```
   export SERPAPI_KEY=your_api_key_here
   ```

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
- **Coordinator Agent**: Main entry point that delegates to specialized agents
- **Weather Agent**: Handles weather queries and unit preferences
- **Greeting Agent**: Processes greetings and salutations
- **Farewell Agent**: Manages conversation closings

## Custom Tools

- `search_web`: Searches the web using SERPAPI
- `get_weather_stateful`: Provides weather information with user preference support
- `set_temperature_unit`: Updates user preferences for temperature units
- `say_hello`: Generates greetings
- `say_goodbye`: Creates farewell messages

## License

Apache License 2.0 