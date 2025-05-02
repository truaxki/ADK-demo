# imports
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm 

# set the agent model
AGENT_MODEL = "openai/o3-mini-2025-01-31"
# AGENT_MODEL = "ollama/gemma3:1b"

# Root agent using auto-discovered tools
reasoning_agent = Agent(
    name="reasoning_agent",
    model=LiteLlm(model=AGENT_MODEL),
    description="I reason with the user. Your model is openai/o3-mini-2025-01-31.",
    instruction="You are a helpful assistant, you will reason with the user and help them with their questions."
)