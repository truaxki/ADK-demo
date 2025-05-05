# Astra - Personal AI Assistant

Astra is a personal AI assistant built with the Google Agent Development Kit (ADK).

## Configuration

Astra uses environment variables for configuration. You can set these in a `.env` file in the root directory. Here are the available configuration options:

### Session Configuration

```
# Application identification
ASTRA_APP_NAME=astra
ASTRA_USER_ID=your_name
ASTRA_SESSION_ID=development

# Default model to use
ASTRA_DEFAULT_MODEL=openai/gpt-4o-mini

# Default preferences
ASTRA_DEFAULT_TEMPERATURE_UNIT=Fahrenheit
```

### API Keys

```
# API keys for various services
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
SERPER_API_KEY=your_serper_api_key
```

## Sub-agents

Astra includes several specialized sub-agents that handle specific domains:

### Weather Agent

Provides real-time weather information and forecasts for locations worldwide. [See details](./weather_agent/README.md).

### Travel Agent

Helps manage and answer questions about travel itineraries, with the ability to check weather conditions at destinations by using the Weather Agent. [See details](./travel_agent/README.md).

## Agent Collaboration

One of Astra's key features is the ability for sub-agents to collaborate and delegate tasks to each other:

### Sub-agent Delegation

- Sub-agents can use other sub-agents as tools to complete specialized tasks
- For example, the Travel Agent can access the Weather Agent to provide weather information for destinations in the itinerary
- This delegation happens through the ADK's tool-calling mechanism, ensuring seamless integration

### Implementation Example

```python
# In travel_agent/agent.py
from google.adk.tools.agent_tool import AgentTool
from astra.weather_agent.agent import weather_agent

# Configure the Travel Agent with the Weather Agent as a tool
travel_concierge_agent = Agent(
    name="travel_concierge_agent",
    model=LiteLlm(model=MODEL_GPT_4O_MINI),
    description="Agent to provide travel concierge content and information.",
    instruction=get_travel_agent_instruction(),
    tools=[
        AgentTool(agent=weather_agent)
    ],
)
```

## Development

### Adding New Configuration Values

To add new configuration values:

1. Add them to the `.env` file
2. Update the `config.py` file to include the new values
3. Import the values where needed

### Adding New Sub-agents

To add a new sub-agent:

1. Create a new directory following the standard agent structure
2. Implement the agent with clear instructions on when to delegate to other agents
3. Register the agent as a tool in the parent agent if needed

## Architecture

### Core Principles
- **Modular Agent Design**: Each agent (including Astra and all sub-agents) is self-contained in its own directory
- **Clear Separation of Concerns**: Each agent has distinct responsibilities
- **Consistent Structure**: All agents follow the same folder structure pattern
- **Hierarchical Organization**: Sub-agents are nested directly within their parent agent's directory

### Standard Agent Structure
Every agent (including Astra and all sub-agents) follows this standard structure:

```
agent_name/
├── __init__.py         # Module initialization
├── agent.py            # Agent implementation
├── prompt.py           # Prompts used by the agent
├── tools.py            # Tools specific to this agent
├── README.md           # Documentation for this agent
└── subagent_name/      # Sub-agent directories (if applicable)
    ├── __init__.py     # Each sub-agent follows the same structure
    ├── agent.py
    └── ...
```

### Astra Hierarchy
```
astra/                          # Root agent
├── __init__.py                 # Module initialization
├── agent.py                    # Astra agent implementation
├── prompt.py                   # Astra prompts
├── tools.py                    # Astra-specific tools
├── README.md                   # This documentation
├── shared_libraries/           # Common utilities used across agents
│   ├── __init__.py
│   └── types.py                # Shared data models/schemas
├── travel_agent/               # Travel planning sub-agent
│   ├── __init__.py
│   ├── agent.py                # Travel agent implementation
│   ├── prompt.py               # Travel agent prompts
│   ├── tools.py                # Travel-specific tools
│   ├── README.md               # Travel agent documentation
│   └── itenerary.json          # Sample travel itinerary
├── weather_agent/              # Weather information sub-agent
│   ├── __init__.py
│   ├── agent.py                # Weather agent implementation
│   ├── prompt.py               # Weather agent prompts
│   ├── tools.py                # Weather-specific tools
│   └── README.md               # Weather agent documentation
└── other_agents/               # Additional specialized agents
```

## Agent Development Guidelines

### Agent Implementation (agent.py)
- Each `agent.py` should define a single agent
- The agent should be instantiated with the appropriate model, description, and tools
- Import prompts from the local `prompt.py`
- Import tools from the local `tools.py`

Example:
```python
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .prompt import AGENT_INSTRUCTIONS
from .tools import agent_specific_tool
from astra.other_agent.agent import other_agent  # Import another agent as a tool

agent_name = Agent(
    model="gemini-2.0-flash",
    name="agent_name",
    description="Description of what this agent does",
    instruction=AGENT_INSTRUCTIONS,
    tools=[
        agent_specific_tool,
        AgentTool(agent=other_agent)  # Use another agent as a tool
    ]
)
```

### Agent Prompts (prompt.py)
- Contain constant string variables with the agent instructions
- Follow naming convention: `AGENT_NAME_INSTR`
- Include clear guidance on when to use tools and sub-agents
- For agents that delegate to others, specify exactly when and how to use other agents

### Agent Tools (tools.py)
- Implement tools specific to the agent's domain
- Use the ADK Tool interface 
- Tools can wrap functions, APIs, or other agents

## Getting Started

### Prerequisites
- Google ADK
- Python 3.9+

### Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables in a `.env` file
4. Run the application: `python -m astra.main`

### Usage
```python
from astra.agent import astra_agent

# Initialize the agent
response = astra_agent.generate_content("Help me plan a trip to Japan")

# Ask about weather at a travel destination
response = astra_agent.generate_content("What's the weather like in Tokyo for my upcoming trip?")
``` 