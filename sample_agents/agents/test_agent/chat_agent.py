# imports
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm 
from adktools import discover_adk_tools
import test_agent.tools

# set the agent model
AGENT_MODEL = "openai/gpt-4o-mini"
# AGENT_MODEL = "ollama/gemma3:1b"

# Root agent using auto-discovered tools
chat_agent = Agent(
    name="chat_agent",
    model=LiteLlm(model=AGENT_MODEL),
    description="I chat with the user. Your model is openai/gpt-4o-mini.",
    instruction="You are a helpful assistant, you will greet the user with your name and ask them how you can help them today.",
    tools=discover_adk_tools(test_agent.tools)
)