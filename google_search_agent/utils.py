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
import os
import requests
import json

def get_weather_stateful(city: str, tool_context: ToolContext) -> dict:
    """Retrieves weather, converts temp unit based on session state."""
    print(f"--- Tool: get_weather_stateful called for {city} ---")

    # --- Read preference from state ---
    preferred_unit = tool_context.state.get("user_preference_temperature_unit", "Celsius") # Default to Celsius
    print(f"--- Tool: Reading state 'user_preference_temperature_unit': {preferred_unit} ---")

    city_normalized = city.lower().replace(" ", "")

    # Mock weather data (always stored in Celsius internally)
    mock_weather_db = {
        "newyork": {"temp_c": 25, "condition": "sunny"},
        "london": {"temp_c": 15, "condition": "cloudy"},
        "tokyo": {"temp_c": 18, "condition": "light rain"},
    }

    if city_normalized in mock_weather_db:
        data = mock_weather_db[city_normalized]
        temp_c = data["temp_c"]
        condition = data["condition"]

        # Enhanced reporting about unit conversion
        if preferred_unit == "Fahrenheit":
            temp_value = (temp_c * 9/5) + 32
            temp_unit = "°F"
            report = f"The weather in {city.capitalize()} is {condition} with a temperature of {temp_value:.0f}{temp_unit} (converted from {temp_c}°C)."
        else:
            temp_value = temp_c
            temp_unit = "°C"
            report = f"The weather in {city.capitalize()} is {condition} with a temperature of {temp_value:.0f}{temp_unit}."

        result = {"status": "success", "report": report}
        print(f"--- Tool: Generated report in {preferred_unit}. Result: {result} ---")

        # Example of writing back to state (optional for this tool)
        tool_context.state["last_city_checked_stateful"] = city
        print(f"--- Tool: Updated state 'last_city_checked_stateful': {city} ---")

        return result
    else:
        # Handle city not found
        error_msg = f"Sorry, I don't have weather information for '{city}'."
        print(f"--- Tool: City '{city}' not found. ---")
        return {"status": "error", "error_message": error_msg}


def say_hello(name: str = "there") -> str:
    """Provides a simple greeting, optionally addressing the user by name.

    Args:
        name (str, optional): The name of the person to greet. Defaults to "there".

    Returns:
        str: A friendly greeting message.
    """
    print(f"--- Tool: say_hello called with name: {name} ---")
    return f"Hello, {name}!"


def say_goodbye() -> str:
    """Provides a simple farewell message to conclude the conversation."""
    print(f"--- Tool: say_goodbye called ---")
    return "Goodbye! Have a great day."


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

def search_web(query: str) -> dict:
    """Search the web using SERPAPI for the given query.
    
    Args:
        query (str): The search query to look up
        
    Returns:
        dict: A dictionary containing the search results
    """
    print(f"--- Tool: search_web called with query: {query} ---")
    
    # Get the API key from environment variables
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        return {
            "status": "error",
            "error_message": "SERPAPI_KEY environment variable not set."
        }
    
    # Prepare the request to SERPAPI
    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google"
    }
    
    try:
        # Make the request
        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the response
        results = response.json()
        
        # Extract the most relevant information
        organic_results = results.get("organic_results", [])
        answer_box = results.get("answer_box", {})
        knowledge_graph = results.get("knowledge_graph", {})
        
        # Format the results for easier consumption
        formatted_results = {
            "status": "success",
            "query": query,
            "top_results": [
                {
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", "")
                } for result in organic_results[:5]  # Limit to top 5 results
            ]
        }
        
        # Add featured snippet or knowledge graph if available
        if answer_box:
            formatted_results["featured_snippet"] = {
                "title": answer_box.get("title", ""),
                "answer": answer_box.get("answer", ""),
                "snippet": answer_box.get("snippet", "")
            }
        
        if knowledge_graph:
            formatted_results["knowledge_graph"] = {
                "title": knowledge_graph.get("title", ""),
                "description": knowledge_graph.get("description", "")
            }
        
        return formatted_results
        
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Error searching the web: {str(e)}"
        }
    except json.JSONDecodeError:
        return {
            "status": "error",
            "error_message": "Error parsing search results."
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Unexpected error: {str(e)}"
        } 