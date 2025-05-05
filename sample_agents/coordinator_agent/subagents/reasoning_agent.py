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

# --- Reasoning Agent ---
reasoning_agent = None
try:
    reasoning_agent = Agent(
        name="reasoning_agent",
        model=LiteLlm(model="openai/o3-mini-2025-01-31"),
        description="I reason with the user. Your model is openai/o3-mini-2025-01-31.",
        instruction="You are a helpful assistant, you will reason with the user and help them with their questions."
    )   
    print(f"✅ Agent '{reasoning_agent.name}' created using model '{reasoning_agent.model}'.")
except Exception as e:
    print(f"❌ Could not create Reasoning agent. Check API Key ({reasoning_agent.model}). Error: {e}") 