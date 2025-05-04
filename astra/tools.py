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

"""Tools for the Astra agent.

This file contains direct function-based tools used by the main Astra agent.
These are general-purpose tools that don't belong to any specific domain.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import requests

from google.adk.tools.tool import Tool

# --- Memory Tool ---

# Simple in-memory storage for the demo
_memory_storage = {}

def remember(key: str, value: str) -> Dict[str, str]:
    """Store information in Astra's memory.
    
    Args:
        key: The identifier for the information
        value: The information to store
        
    Returns:
        Dict with status of the operation
    """
    _memory_storage[key] = value
    return {
        "status": "success",
        "message": f"I've stored that information under '{key}'."
    }

def recall(key: str) -> Dict[str, str]:
    """Retrieve information from Astra's memory.
    
    Args:
        key: The identifier for the information to retrieve
        
    Returns:
        Dict with the retrieved information or error
    """
    if key in _memory_storage:
        return {
            "status": "success", 
            "value": _memory_storage[key]
        }
    else:
        return {
            "status": "error",
            "message": f"I don't have any information stored under '{key}'."
        }

# Combine both functions into a single memory tool
def memory_function(action: str, key: str, value: Optional[str] = None) -> Dict[str, str]:
    """Store or retrieve information from Astra's memory.
    
    Args:
        action: Either "store" or "retrieve"
        key: The identifier for the information
        value: The information to store (only needed for "store" action)
        
    Returns:
        Dict with the result of the operation
    """
    if action == "store":
        if value is None:
            return {"status": "error", "message": "No value provided to store."}
        return remember(key, value)
    elif action == "retrieve":
        return recall(key)
    else:
        return {"status": "error", "message": f"Unknown action: {action}. Use 'store' or 'retrieve'."}

memory_tool = Tool(
    name="memory_tool",
    description="Store or retrieve information from Astra's memory",
    function=memory_function
)

# --- Web Search Tool ---

def web_search(query: str, num_results: int = 5) -> Dict:
    """Search the web for information on a topic.
    
    Args:
        query: The search query
        num_results: Number of results to return (default 5)
        
    Returns:
        Dict with search results
    """
    # Check for API key
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        return {
            "status": "error",
            "message": "Web search is unavailable. API key not configured."
        }
    
    # Call SerpAPI
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": api_key,
        "num": num_results
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # Extract the organic results
        if "organic_results" in data:
            results = []
            for result in data["organic_results"][:num_results]:
                results.append({
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", "")
                })
            
            return {
                "status": "success",
                "query": query,
                "results": results
            }
        else:
            return {
                "status": "error",
                "message": "No results found.",
                "query": query
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error searching the web: {str(e)}",
            "query": query
        }

web_search_tool = Tool(
    name="web_search_tool",
    description="Search the web for real-time information on any topic",
    function=web_search
)

# --- User Profile Tool ---

# Simple profile storage for the demo
_user_profile = {
    "preferences": {},
    "last_updated": None
}

def update_profile(preference_key: str, preference_value: str) -> Dict:
    """Update a user preference in their profile.
    
    Args:
        preference_key: The preference category (e.g., "temperature_unit", "travel_style")
        preference_value: The preference value
        
    Returns:
        Dict with the result of the operation
    """
    _user_profile["preferences"][preference_key] = preference_value
    _user_profile["last_updated"] = datetime.now().isoformat()
    
    return {
        "status": "success",
        "message": f"Updated {preference_key} preference to {preference_value}",
        "profile": _user_profile
    }

def get_profile() -> Dict:
    """Retrieve the user's current profile.
    
    Returns:
        Dict with the user profile information
    """
    return {
        "status": "success",
        "profile": _user_profile
    }

def profile_function(action: str, preference_key: Optional[str] = None, preference_value: Optional[str] = None) -> Dict:
    """Update or retrieve user profile information.
    
    Args:
        action: Either "update" or "get"
        preference_key: The preference to update (only for "update" action)
        preference_value: The new preference value (only for "update" action)
        
    Returns:
        Dict with the result of the operation
    """
    if action == "update":
        if not preference_key or not preference_value:
            return {"status": "error", "message": "Missing preference key or value for update."}
        return update_profile(preference_key, preference_value)
    elif action == "get":
        return get_profile()
    else:
        return {"status": "error", "message": f"Unknown action: {action}. Use 'update' or 'get'."}

profile_tool = Tool(
    name="profile_tool",
    description="Update or retrieve user profile information",
    function=profile_function
) 