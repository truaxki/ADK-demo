"""Astra - Personal AI Agent Framework.

Astra is a modular framework for building hierarchical AI agents that 
can work together to solve complex tasks across different domains.
"""

from .agent import root_agent
from astra.travel_agent import travel_concierge_agent, user_profile, itinerary
from astra.weather_agent import weather_agent
from astra.db_manager_agent import db_manager_agent

__version__ = "0.1.0"
__all__ = ["root_agent", "travel_concierge_agent", "user_profile", "itinerary", "weather_agent", "db_manager_agent"]
