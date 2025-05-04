#!/usr/bin/env python3
"""Test script for travel agent."""

import sys
import os
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Import travel agent components
try:
    from astra.travel_agent.agent import travel_concierge_agent, user_profile, itinerary
    
    # Print some information to verify it loaded
    print("Travel Agent Test")
    print("-" * 50)
    print(f"User: {user_profile.get('name', 'Unknown')}")
    print(f"Travel dates: {itinerary.get('travel_dates', {}).get('start')} to {itinerary.get('travel_dates', {}).get('end')}")
    print(f"Agent model: {travel_concierge_agent.model}")
    print(f"Agent name: {travel_concierge_agent.name}")
    print("-" * 50)
    
    # Success
    print("✅ Travel agent loaded successfully!")
    
except Exception as e:
    print(f"❌ Error loading travel agent: {e}")
    import traceback
    traceback.print_exc() 