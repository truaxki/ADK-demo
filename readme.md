# ADK Testing Repository

The purpose of this repository is to test Google's Agent Development Kit and explore tool integrations in a multi-agent architecture.

## Multi-Agent Orchestration System

This repository demonstrates an orchestrated multi-agent system where a coordinator agent manages specialized sub-agents. The main focus is on:

- **Coordinator-based Orchestration:** Building a system where a central agent delegates tasks to specialized agents
- **Multi-Agent Architecture:** Demonstrating how multiple agents can work together through delegation
- **Tool Development & Testing:** Creating a framework for developing and testing agentic tools
- **API Integrations:** Connecting agents to external services like weather data and web search

The guardrail implementations (block_keyword_guardrail, block_tool_guardrail) are sample agents for future reference and development.

## Core Components

### Coordinator Agent

The main agent that:
- Manages conversation flow
- Delegates tasks to specialized sub-agents
- Integrates external API tools
- Maintains conversation context

### Sub-Agents

- **Greeting Agent:** Handles user greetings
- **Farewell Agent:** Manages conversation closings
- **Weather Agent:** Provides weather information

### Tool Integrations

The system demonstrates how to build and integrate various tools for agents:
- **Weather API Tools:** Real-time weather data retrieval
- **Web Search Tools:** Up-to-date information retrieval
- **State Management Tools:** Maintaining user preferences

## Weather & Search Agent Demo

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