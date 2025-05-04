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

Astra includes several specialized sub-agents:

### Weather Agent

Provides real-time weather information. [See details](./weather_agent/README.md).

## Development

### Adding New Configuration Values

To add new configuration values:

1. Add them to the `.env` file
2. Update the `config.py` file to include the new values
3. Import the values where needed

## Overview
Astra is a personal agent framework that connects users with specialized sub-agents designed to handle specific domains and tasks. Acting as a coordinator, Astra routes user requests to the appropriate specialized agents based on the nature of the task.

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
├── travel_concierge/           # Travel planning sub-agent
│   ├── __init__.py
│   ├── agent.py                # Travel concierge implementation
│   ├── prompt.py               # Travel concierge prompts
│   ├── tools.py                # Travel-specific tools
│   ├── README.md               # Travel concierge documentation
│   ├── inspiration/            # Travel inspiration sub-agent
│   ├── planning/               # Trip planning sub-agent
│   └── booking/                # Reservation sub-agent
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
from .prompt import AGENT_INSTRUCTIONS
from .tools import agent_specific_tool

agent_name = Agent(
    model="gemini-2.0-flash",
    name="agent_name",
    description="Description of what this agent does",
    instruction=AGENT_INSTRUCTIONS,
    tools=[agent_specific_tool]
)
```

### Agent Prompts (prompt.py)
- Contain constant string variables with the agent instructions
- Follow naming convention: `AGENT_NAME_INSTR`
- Include clear guidance on when to use tools and sub-agents

### Agent Tools (tools.py)
- Implement tools specific to the agent's domain
- Use the ADK Tool interface 
- Tools can wrap functions, APIs, or other agents

### Sub-agent Integration
- Parent agents should import sub-agents as tools
- Use `AgentTool` to wrap sub-agents for use in parent agents

Example:
```python
# In parent_agent/tools.py
from google.adk.tools.agent_tool import AgentTool
from .subagent_name.agent import subagent

subagent_tool = AgentTool(agent=subagent)
```

## Project Documentation

Beyond the README files in each agent directory, we maintain more comprehensive documentation:

1. **Architecture Document**: High-level overview of the system structure
2. **Developer Guides**: In the `/docs` directory for contributor onboarding
3. **API Documentation**: Auto-generated from docstrings
4. **Project Wiki**: For evolving design decisions and discussions

## Getting Started

### Prerequisites
- Google ADK
- Python 3.9+

### Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables

### Usage
```python
from astra.agent import astra_agent

# Initialize the agent
response = astra_agent.generate_content("Help me plan a trip to Japan")
``` 