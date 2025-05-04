"""Astra - Personal AI Agent.

Core agent implementation for the Astra personal AI assistant.
"""

import os
from pathlib import Path

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# Import prompt instructions
from .prompt import ASTRA_BASIC_TEST_INSTR

# Configure model constants
MODEL_GEMINI_FLASH = "gemini-2.0-flash"
MODEL_GPT_4_MINI = "openai/gpt-4o-mini"

# Load environment variables from .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Proceed without dotenv if not installed

# Initialize the Astra agent
root_agent = Agent(
    name="astra",
    model=LiteLlm(model=MODEL_GPT_4_MINI),
    description="Astra is a personal AI assistant that helps users with information and tasks.",
    instruction=ASTRA_BASIC_TEST_INSTR,
    tools=[],
    sub_agents=[],
)
