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
import requests
import json

def search_web(query: str) -> dict:
    """Simple web search using Serper.dev API.
    
    Args:
        query (str): The search query to look up
        
    Returns:
        dict: The search results (raw API response)
    """
    print(f"Searching for: {query}")
    
    # Sanitize the query to avoid JSON parsing issues
    if not query or not isinstance(query, str):
        return {"error": "Invalid query parameter. Please provide a valid search string."}
    
    # Trim and normalize the query
    query = query.strip()
    
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        return {"error": "SERPER_API_KEY not set"}
    
    # Correct endpoint for Serper API based on documentation
    url = "https://serpapi.com/search"
    
    # Use API key as a parameter for SerpAPI
    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google"
    }
    
    try:
        # Switch to GET request for SerpAPI
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        return {
            "error": f"HTTP Error: {e}", 
            "url": url, 
            "status_code": e.response.status_code
        }
    except Exception as e:
        return {"error": str(e)} 