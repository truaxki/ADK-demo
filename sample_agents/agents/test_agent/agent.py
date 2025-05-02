# imports
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# import agents
from test_agent.chat_agent import chat_agent
from coordinator_agent.reasoning_agent import reasoning_agent

# set the agent model
AGENT_MODEL = "claude-3-7-sonnet-20250219"

# AGENT_MODEL = "ollama/deepseek-r1:1.5b"

# Root agent using auto-discovered tools
root_agent = Agent(
    name="coordination_agent",
    model=LiteLlm(model=AGENT_MODEL),
    description="I coordinate the actions of the other agents, your model is claude-3-7-sonnet-20250219.",
    instruction="You are a helpful assistant, you will greet the user with your name and ask them how you can help them today.",
    sub_agents=[chat_agent, reasoning_agent]
)