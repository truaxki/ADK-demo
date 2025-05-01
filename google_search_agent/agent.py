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

APP_NAME="google_search_agent"
USER_ID="Kirk"
SESSION_ID="1234"

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
MODEL_GPT_4O_MINI = "openai/gpt-4o-mini"

# --- Greeting Agent ---
greeting_agent = None
try:
    greeting_agent = Agent(
        # Using a potentially different/cheaper model for a simple task
        # model = MODEL_GEMINI_2_0_FLASH,
        model=LiteLlm(model=MODEL_GPT_4O_MINI), # If you would like to experiment with other models 
        name="greeting_agent",
        instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting to the user. "
                    "Use the 'say_hello' tool to generate the greeting. "
                    "If the user provides their name, make sure to pass it to the tool. "
                    "Do not engage in any other conversation or tasks.",
        description="Handles simple greetings and hellos using the 'say_hello' tool.", # Crucial for delegation
        tools=[say_hello],
    )
    print(f"✅ Agent '{greeting_agent.name}' created using model '{greeting_agent.model}'.")
except Exception as e:
    print(f"❌ Could not create Greeting agent. Check API Key ({greeting_agent.model}). Error: {e}")

# --- Farewell Agent ---
farewell_agent = None
try:
    farewell_agent = Agent(
        # Can use the same or a different model
        # model = MODEL_GEMINI_2_0_FLASH,
        model=LiteLlm(model=MODEL_GPT_4O_MINI), # If you would like to experiment with other models
        name="farewell_agent",
        instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message. "
                    "Use the 'say_goodbye' tool when the user indicates they are leaving or ending the conversation "
                    "(e.g., using words like 'bye', 'goodbye', 'thanks bye', 'see you'). "
                    "Do not perform any other actions.",
        description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.", # Crucial for delegation
        tools=[say_goodbye],
    )
    print(f"✅ Agent '{farewell_agent.name}' created using model '{farewell_agent.model}'.")
except Exception as e:
    print(f"❌ Could not create Farewell agent. Check API Key ({farewell_agent.model}). Error: {e}")
    
    
# --- Weather Agent ---
weather_agent = None
try:
    weather_agent = Agent(
        name="weather_agent",
        model=LiteLlm(model=MODEL_GPT_4O_MINI),
        description="Agent to provide weather information.",
        instruction="You are the Weather Agent. Your ONLY task is to provide weather information.",
        tools=[get_weather_stateful, set_temperature_unit],
    )
    print(f"✅ Agent '{weather_agent.name}' created using model '{weather_agent.model}'.")
except Exception as e:
    print(f"❌ Could not create Weather agent. Check API Key ({weather_agent.model}). Error: {e}")  


# --- Root Agent ---
# No built-in tools, using our custom SERPAPI search function instead
# This agent supports voice-to-voice interactions when run with 'adk web'
root_agent = Agent(
    name="coordinator_agent",
    model=LiteLlm(model=MODEL_GPT_4O_MINI),  # Using OpenAI model for coordination
    description="Main coordinator agent that delegates tasks to specialized sub-agents.",
    instruction="You are a coordinator agent that manages specialized sub-agents. "
               "For web searches and information lookups, use the 'search_web' function directly. "
               "For weather information, delegate to the 'weather_agent'. "
               "For greetings, delegate to 'greeting_agent'. "
               "For farewells, delegate to 'farewell_agent'. "
               "When speaking to users, use natural, conversational language that works well for both text and voice interactions.",
    tools=[search_web],  # Custom search tool that uses SERPAPI
    sub_agents=[greeting_agent, farewell_agent, weather_agent],
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

