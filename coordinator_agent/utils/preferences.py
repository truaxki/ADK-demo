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

from google.adk.tools.tool_context import ToolContext

def set_temperature_unit(unit: str, tool_context: ToolContext) -> dict:
    """Updates the user's preferred temperature unit in session state.
    
    Args:
        unit (str): The preferred temperature unit ("Celsius" or "Fahrenheit")
        tool_context (ToolContext): Context containing session state
        
    Returns:
        dict: Status of the operation
    """
    normalized_unit = unit.strip().capitalize()
    if normalized_unit not in ["Celsius", "Fahrenheit"]:
        return {
            "status": "error", 
            "error_message": f"Invalid temperature unit: '{unit}'. Please use 'Celsius' or 'Fahrenheit'."
        }
    
    # Update the preference in state
    tool_context.state["user_preference_temperature_unit"] = normalized_unit
    
    return {
        "status": "success",
        "message": f"Your temperature unit preference has been updated to {normalized_unit}."
    } 