# Astra Architecture Specification

## 1. Introduction

This document provides a detailed technical specification for the Astra agent architecture. It serves as the authoritative reference for developers working on the project.

## 2. System Overview

Astra is a hierarchical multi-agent system built on the Google Agent Development Kit (ADK). It consists of a main coordinator agent that delegates tasks to specialized sub-agents based on user needs.

## 3. Core Components

### 3.1 Agent Framework

Astra is built on the Google ADK, which provides the following core components:

- **Agent**: The base class for all agents in the system
- **Tool**: The interface for all tools used by agents
- **AgentTool**: A special tool type that wraps an agent for use by another agent

### 3.2 Agent Types

#### 3.2.1 Coordinator Agent
- Primary interface with the user
- Routes requests to appropriate specialized agents
- Maintains conversation context and continuity

#### 3.2.2 Specialist Agents
- Domain-specific expertise (travel, productivity, etc.)
- Can have their own sub-agents for more specific tasks
- Focused on a particular problem domain

### 3.3 Tool Types

#### 3.3.1 Function Tools
- Wrap functions for use by agents
- Used for simple actions like data retrieval or calculations

#### 3.3.2 API Tools
- Interface with external services and APIs
- Handle authentication and data formatting

#### 3.3.3 Agent Tools
- Wrap other agents for use by a parent agent
- Facilitate hierarchical agent architectures

## 4. Directory Structure Specification

### 4.1 Standard Agent Package

Every agent in the system follows this standardized structure:

```
agent_name/
├── __init__.py         # Exports the agent instance and main components
├── agent.py            # Agent implementation and configuration
├── prompt.py           # Agent-specific prompts and instructions
├── tools.py            # Agent-specific tools (not including sub-agents)
├── README.md           # Agent-specific documentation
└── subagent_name/      # Sub-agent directory (if any) - directly under parent
    ├── __init__.py
    ├── agent.py
    └── ...
```

### 4.2 Shared Components

```
shared_libraries/       # Common utilities and types used across agents
├── __init__.py
├── types.py            # Shared data models and schemas
├── utils.py            # Utility functions
└── constants.py        # System-wide constants
```

### 4.3 Documentation

```
docs/
├── ARCHITECTURE.md     # This document
├── CONTRIBUTING.md     # Contributor guidelines
├── API.md              # API documentation
└── agent_guides/       # Detailed guides for each agent type
    ├── astra.md
    ├── travel_concierge.md
    └── ...
```

## 5. Agent Implementation Details

### 5.1 Agent Initialization Pattern

```python
from google.adk.agents import Agent
from .prompt import AGENT_INSTRUCTIONS
from .tools import tool1, tool2

agent_name = Agent(
    model="[MODEL_IDENTIFIER]",
    name="[AGENT_NAME]",
    description="[AGENT_DESCRIPTION]",
    instruction=AGENT_INSTRUCTIONS,
    tools=[tool1, tool2],
    
    # Optional parameters
    disallow_transfer_to_parent=False,
    disallow_transfer_to_peers=False,
    output_schema=None,  # Optional schema for structured output
    output_key=None,     # Key for output when used as a tool
    generate_content_config={},  # Model-specific configuration
)
```

### 5.2 Sub-agent Integration

```python
# In parent_agent/tools.py
from google.adk.tools.agent_tool import AgentTool
from parent_agent.subagent_name.agent import subagent

subagent_tool = AgentTool(
    agent=subagent,
    # Optional: Override name, description, etc.
)
```

### 5.3 Tool Implementation

```python
# In agent/tools.py
from google.adk.tools.tool import Tool

def tool_function(param1, param2):
    """Tool documentation.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        The result of the tool execution
    """
    # Tool implementation
    return result

tool_name = Tool(
    name="tool_name",
    description="Tool description for the agent",
    function=tool_function
)
```

## 6. Agent Prompt Design

Agent prompts should follow this structure:

```python
AGENT_NAME_INSTR = """
You are [role description].
Your goal is to [primary objective].

- You will call the tools [tool1], [tool2], etc. when appropriate:
  - Use [tool1] for [purpose]
  - Use [tool2] for [purpose]
  
- [Additional guidance on expected behavior]
- [Guidance on when to use sub-agents vs. handling directly]
- [Other important considerations]

Context:
  <user_profile>
  {user_profile}
  </user_profile>

Current time: {_time}
"""
```

## 7. Agent Communication Protocols

### 7.1 Parent-to-Child Communication

When a parent agent calls a sub-agent through an AgentTool:

1. The parent provides a query to the sub-agent
2. The sub-agent processes the query with its own tools and capabilities
3. The sub-agent returns structured output according to its output_schema
4. The parent receives the output under the sub-agent's output_key

### 7.2 Response Formatting

Agents should format responses according to:

1. Their defined output_schema if used as a tool
2. User-friendly natural language if interacting directly with a user

## 8. External Service Integration

### 8.1 API Key Management

API keys and credentials should be:
- Stored in environment variables
- Never hardcoded in the repository
- Loaded at runtime through a secure credentials manager

### 8.2 Rate Limiting and Caching

All external API calls should implement:
- Rate limiting to respect API provider terms
- Caching of responses where appropriate
- Graceful error handling for service unavailability

## 9. Testing Strategy

### 9.1 Unit Testing

- Each tool function should have unit tests
- Mock external services for testing
- Test edge cases and error handling

### 9.2 Integration Testing

- Test interaction between agents
- Verify correct routing of requests
- Simulate user conversations end-to-end

## 10. Deployment Considerations

### 10.1 Environment Configuration

- Development, staging, and production environments
- Feature flags for gradual rollout of capabilities
- Monitoring and logging infrastructure

### 10.2 Scaling

- Stateless design for horizontal scaling
- Agent instance pooling strategies
- Resource allocation guidelines for different agent types

## 11. Future Roadmap

### 11.1 Planned Capabilities

- Additional specialist agents
- Enhanced tool libraries
- Improved coordination strategies

### 11.2 Research Areas

- Context management optimizations
- Multi-turn reasoning improvements
- Agent collaboration patterns 