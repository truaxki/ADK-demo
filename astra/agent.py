"""Astra - Personal AI Agent.

Core agent implementation for the Astra personal AI assistant.
"""

import os
import json
from pathlib import Path
from datetime import datetime

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.agent_tool import AgentTool
from google.genai import types
from google.adk.models.lite_llm import LiteLlm

# Import prompt instructions
from .prompt import ASTRA_AGENT_INSTR, ASTRA_BASIC_TEST_INSTR
from .shared_libraries.search_web import search_web

# Import sub-agents
from .weather_agent.agent import weather_agent

# Define session variables
APP_NAME = "astra"
USER_ID = "default_user"
SESSION_ID = "development"
MODEL_GPT_4_MINI = "openai/gpt-4o-mini"

# Load environment variables from .env
try:
    from dotenv import load_dotenv
    load_dotenv()
    # Override with environment variables if they exist
    APP_NAME = os.getenv("ASTRA_APP_NAME", APP_NAME)
    USER_ID = os.getenv("ASTRA_USER_ID", USER_ID)
    SESSION_ID = os.getenv("ASTRA_SESSION_ID", SESSION_ID)
except ImportError:
    pass  # Proceed without dotenv if not installed

# Load data from the config.json file
def load_config():
    config_path = Path(__file__).parent / "config.json"
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return default values if file not found
        return {
            "user_profile": {"name": "Default User"}
        }

# Get data for prompt
config = load_config()
user_profile = config.get("user_profile", {})
# Always use the current time
current_time = datetime.now().isoformat()

# Initialize the Astra agent
root_agent = Agent(
    name="astra",
    model=LiteLlm(model=MODEL_GPT_4_MINI),
    description="Astra is a personal AI assistant that helps users with information and tasks.",
    instruction=ASTRA_AGENT_INSTR.format(user_profile=json.dumps(user_profile), _time=current_time),
    tools=[search_web, AgentTool(agent=weather_agent)],
    # sub_agents=[weather_agent],
)

# Session and Runner
session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
