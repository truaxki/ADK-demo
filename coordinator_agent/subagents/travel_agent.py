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
from ..utils import search_web

# Constants
MODEL_GPT_4O_MINI = "openai/gpt-4o-mini"

# Define a function to handle pre-trip planning requests
def handle_pre_trip_planning(query):
    """Forwards pre-trip planning queries to the pre-trip agent."""
    # In a real implementation, this would interact with the pre-trip agent's API
    # For now, just return a simple response confirming the query was received
    return f"Pre-trip planning query received: {query}"

# Import pre-trip agents
try:
    from .pre_trip.agent import pre_trip_agent, what_to_pack_agent
    pre_trip_agents_available = True
    print("✅ Pre-trip agents imported successfully.")
except ImportError as e:
    pre_trip_agents_available = False
    print(f"⚠️ Could not import pre-trip agents. Error: {e}")

# --- Travel Agent ---
travel_agent = None
try:
    # Prepare tools list
    tools = [search_web]
    
    # Add pre-trip specific tools if available
    if pre_trip_agents_available:
        tools.append(handle_pre_trip_planning)
    
    travel_agent = Agent(
        name="travel_agent",
        model=LiteLlm(model=MODEL_GPT_4O_MINI),
        description="Agent that provides travel recommendations, information, and planning assistance.",
        instruction="""You are the Travel Agent. Your task is to assist users with their travel needs. 
This includes providing information about destinations, flight options, 
hotel recommendations, tourist attractions, and general travel planning. 
Use the 'search_web' tool to find real-time travel information.

When a user asks about pre-trip planning, such as what to pack or visa requirements,
use the 'handle_pre_trip_planning' function with their specific query.

Be friendly, informative, and helpful in suggesting travel options based on user preferences. 
When making recommendations, consider factors like budget, season, interests, and 
travel style when the user provides such information.""",
        tools=tools,
    )
    print(f"✅ Agent '{travel_agent.name}' created using model '{travel_agent.model}'.")
except Exception as e:
    print(f"❌ Could not create Travel agent. Check API Key ({travel_agent.model}). Error: {e}") 