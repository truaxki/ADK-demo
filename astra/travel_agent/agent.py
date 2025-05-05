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
import json
from datetime import datetime
from pathlib import Path
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool

from astra.travel_agent.prompt import TRAVEL_AGENT_INSTR
from astra.weather_agent.agent import weather_agent

def load_config():
    """Load user profile from config.json."""
    config_path = Path(__file__).parent.parent / "config.json"
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"user_profile": {"name": "Default User", "interests": [], "preferences": {}}}

def load_itinerary():
    """Load travel itinerary from itenerary.json."""
    config_path = Path(__file__).parent / "itenerary.json"
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"itinerary": {"travel_dates": {"start": "2025-06-15", "end": "2025-07-15"}, "items": []}}

def get_travel_agent_instruction():
    """Get the travel agent instruction with context."""
    # Load data
    user_profile = load_config().get("user_profile", {})
    travel_itinerary = load_itinerary()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Format the instruction with double braces to escape the JSON format
    instruction = TRAVEL_AGENT_INSTR.format(
        user_profile=json.dumps(user_profile, indent=2),
        travel_itinerary=json.dumps(travel_itinerary, indent=2),
        _time=current_time
    )
    
    # Add an extra prompt to use the itinerary function
    instruction += f"\n\nIMPORTANT: Use the get_itinerary function to access the complete travel itinerary information."
    
    return instruction

# Load data for direct access
user_profile = load_config().get("user_profile", {})
itinerary = load_itinerary().get("itinerary", {})

# Constants
MODEL_GPT_4O_MINI = "openai/gpt-4o-mini"

# Create ADK agent with travel context
travel_concierge_agent = Agent(
    name="travel_concierge_agent",
    model=LiteLlm(model=MODEL_GPT_4O_MINI),
    description="Agent to provide travel concierge content and information.",
    instruction=get_travel_agent_instruction(),
    tools=[
        AgentTool(agent=weather_agent)
    ],
    sub_agents=[weather_agent]
)
print(f"✅ Agent '{travel_concierge_agent.name}' created using model '{travel_concierge_agent.model}'.") 