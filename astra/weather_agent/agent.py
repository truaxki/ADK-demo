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

import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool
from .tools import get_weather_stateful, set_temperature_unit
from ..db_manager_agent.agent import db_manager_agent

# Constants
MODEL_GPT_4O_MINI = "openai/gpt-4o-mini"

# --- Weather Agent ---
weather_agent = None
try:
    weather_agent = Agent(
        name="weather_agent",
        model=LiteLlm(model=MODEL_GPT_4O_MINI),
        description="Agent to provide real-time weather information from OpenWeatherMap API.",
        instruction="You are the Weather Agent. Your task is to provide real-time weather information "
                   "using the OpenWeatherMap API through the 'get_weather_stateful' tool. "
                   "You can respond to queries about current weather conditions in any city worldwide. "
                   "Users can also set their temperature unit preference (Celsius/Fahrenheit) using "
                   "the 'set_temperature_unit' tool, which you should use when they express such a preference. "
                   "Always provide weather information in a friendly, conversational tone.",
        tools=[get_weather_stateful, set_temperature_unit, AgentTool(agent=db_manager_agent)],
    )
    print(f"✅ Agent '{weather_agent.name}' created using model '{weather_agent.model}'.")
except Exception as e:
    print(f"❌ Could not create Weather agent. Check API Key. Error: {e}") 