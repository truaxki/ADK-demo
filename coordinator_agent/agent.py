# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# @title Import necessary libraries
import os
import sys
from pathlib import Path

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from google.adk.models.lite_llm import LiteLlm # For multi-model support
from google.adk.tools.tool_context import ToolContext

# Import the tool functions from the utils module
from .utils import (
    get_weather_stateful,
    say_hello,
    say_goodbye,
    set_temperature_unit,
    search_web  # Import the new SERPAPI search function
)

# Import sub-agents from the subagents package
from .subagent_name.agent import subagent

# Simple .env file loading
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load from .env file if present
    print("Environment variables loaded.")
except ImportError:
    # Fallback for manual .env loading if python-dotenv is not installed
    env_path = Path('.') / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                key, value = line.split('=', 1)
                os.environ[key] = value
        print("Environment variables loaded manually.")

# Check for required API keys
if not os.getenv("OPENWEATHERMAP_API_KEY"):
    print("⚠️ Warning: OPENWEATHERMAP_API_KEY not set. Weather features will not work.")
    
if not os.getenv("SERPAPI_KEY"):
    print("⚠️ Warning: SERPAPI_KEY not set. Web search features will not work.")

APP_NAME="coordinator_agent"
USER_ID="User"
SESSION_ID="1234"

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
MODEL_GPT_4O_MINI = "openai/gpt-4o-mini"

# --- Root Agent ---
# No built-in tools, using our custom SERPAPI search function instead
# This agent supports voice-to-voice interactions when run with 'adk web'
root_agent = Agent(
    name="coordinator_agent",
    model=LiteLlm(model=MODEL_GPT_4O_MINI),  # Using OpenAI model for coordination
    description="Main coordinator agent that delegates tasks to specialized sub-agents and provides real-time information.",
    instruction="You are a coordinator agent that manages specialized sub-agents. "
               "For web searches and information lookups, use the 'search_web' function directly. "
               "For real-time weather information using OpenWeatherMap API, delegate to the 'weather_agent'. "
               "For greetings, delegate to 'greeting_agent'. "
               "For farewells, delegate to 'farewell_agent'. "
               "For reasoning, delegate to 'reasoning_agent'. "
               "For travel-related questions and recommendations, delegate to the 'travel_agent'. The travel_agent can "
               "help with destination information, flight options, hotel recommendations, tourist attractions, and "
               "pre-trip planning including packing suggestions and travel requirements. "
               "When speaking to users, use natural, conversational language that works well for both text and voice interactions. "
               "Emphasize to users that you provide real-time weather data when they ask about the weather.",
    tools=[search_web],  # Custom search tool that uses SERPAPI
    sub_agents=[greeting_agent, farewell_agent, weather_agent, reasoning_agent, travel_agent],
    output_key="last_response"
)

# To run this agent with voice capabilities:
# 1. Make sure you have installed ADK tools with 'pip install adktools'
# 2. Start the web server with 'adk web'
# 3. Access the web interface and use the microphone button for voice input

# Don't run the agent here when imported - this will cause errors with adk tools
# session_service = InMemorySessionService()
# session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
# runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
# response = runner.run(session)
# print(response)

