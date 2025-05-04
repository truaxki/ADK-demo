"""Tools for the Astra agent.

This module exposes various tools that can be used by the Astra agent.
"""

from .shared_libraries.search_web import search_web

# Create a web search tool function that can be used by the agent
def web_search(search_term: str) -> dict:
    """Search the web for information on a given topic.
    
    Args:
        search_term (str): The search term to look up on the web
        
    Returns:
        dict: A dictionary containing the search results
    """
    return search_web(search_term) 