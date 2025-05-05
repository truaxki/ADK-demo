# Google ADK Demonstration

This repository demonstrates the capabilities of Google's Agent Development Kit (ADK), showcasing a multi-agent architecture through a personal AI assistant named Astra.

## What is the Google Agent Development Kit?

The Agent Development Kit (ADK) is an open-source framework from Google designed to simplify the development of AI agents and multi-agent systems. It provides developers with tools to build, test, evaluate, and deploy agent-based applications with greater flexibility and control.

## What This Demo Showcases

![Agent Architecture Diagram](assets/Screenshot%202025-05-04%20205649.png)

*Diagram showing Astra as the coordinator agent with connections to the travel agent, weather agent, and web search functionality.*

This demonstration focuses on:

- **Astra Personal Assistant:** A configurable personal AI assistant
- **Multi-Agent Architecture:** How specialized sub-agents can work together
- **Agent Delegation:** How agents can use other agents as tools
- **External API Integration:** Connecting agents to services like weather data and web search

### Key Agents in the Demo

- **Astra (Coordinator):** The main agent that manages conversation flow
- **Travel Agent:** Handles travel itinerary questions and planning
- **Weather Agent:** Provides weather information for locations
- **More specialized agents:** Each handling specific domains

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- uv package manager (instructions below)
- Google ADK CLI (will be installed in the steps below)

### Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/truaxki/adk-demo.git
   cd adk-demo
   ```

2. **Install uv:**
   
   uv is a fast, reliable Python package installer and resolver. This project uses uv to manage dependencies.

   ```bash
   # For Windows (PowerShell)
   curl.exe -L --output uv-installer.ps1 https://astral.sh/uv/install.ps1
   powershell -ExecutionPolicy Bypass -File .\uv-installer.ps1
   # Restart your terminal after installation
   
   # For macOS/Linux
   curl -L --proto '=https' --tlsv1.2 -sSf https://astral.sh/uv/install.sh | sh
   source ~/.cargo/env
   ```

3. **Create and activate a virtual environment:**
   ```bash
   # With uv
   uv venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

4. **Install dependencies using uv:**
   ```bash
   uv pip install -e .
   ```

   This will install all dependencies defined in the pyproject.toml file, including google-adk, litellm, and other required packages.

5. **Create a `.env` file in the repository root with your API keys:**
   ```
   # LLM API (choose one based on your preference)
   OPENAI_API_KEY=your_openai_key_here
   # or
   GOOGLE_API_KEY=your_google_key_here
   # or
   ANTHROPIC_API_KEY=your_anthropic_key_here
   
   # External Services
   OPENWEATHERMAP_API_KEY=your_openweathermap_key_here
   SERPER_API_KEY=your_serper_api_key_here
   
   # Astra Configuration
   ASTRA_APP_NAME=astra
   ASTRA_USER_ID=your_name
   ASTRA_SESSION_ID=development
   ASTRA_DEFAULT_MODEL=openai/gpt-4o-mini
   ASTRA_DEFAULT_TEMPERATURE_UNIT=Fahrenheit
   ```

## Running the Demo

### Using the ADK Web Interface (Recommended)

The ADK web interface provides a chat UI to interact with the agents:

```bash
adk web
```

This will start a local web server, typically at http://localhost:8080. Open this URL in your browser to interact with Astra.

### Using the ADK CLI

Alternatively, you can run the agent directly in the terminal:

```bash
adk run astra/agent.py
```

## Example Interactions

Here are some examples of what you can ask Astra:

### General Questions
- "What can you help me with?"
- "Tell me about yourself"

### Weather Queries
- "What's the weather like in San Francisco?"
- "Will it rain in New York tomorrow?"
- "I prefer temperatures in Celsius"

### Travel Questions
- "What's on my travel itinerary?"
- "When am I going to Rio de Janeiro?"
- "What's the weather like at my first destination?"

### Using Agent Delegation
- Ask travel questions that require weather information to see how the Travel Agent delegates to the Weather Agent

## Project Structure

```
astra/                          # Main assistant
├── agent.py                    # Astra agent implementation
├── prompt.py                   # Astra prompts
├── travel_agent/               # Travel planning sub-agent
│   ├── agent.py                # Travel agent implementation
│   └── itenerary.json          # Sample travel itinerary
├── weather_agent/              # Weather information sub-agent
│   └── agent.py                # Weather agent implementation
└── other_agents/               # Additional specialized agents

# Configuration files
.env                            # Environment variables
pyproject.toml                  # Project dependencies and metadata
```

## Resources

- [Google ADK Documentation](https://github.com/google/agent-development-kit)
- [ADK Blog Announcement](https://developers.googleblog.com/en/agent-development-kit-easy-to-build-multi-agent-applications/)
- [uv Documentation](https://github.com/astral-sh/uv)

## License

This demo is provided under the Apache 2.0 License.