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