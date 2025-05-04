#!/usr/bin/env python3
"""Example for using the Travel Agent with ADK."""

import json
import sys
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from google.adk.agents import Agent
    from astra.travel_agent.agent import travel_concierge_agent, user_profile, itinerary
except ImportError:
    print("Error: This example requires the Agent Development Kit (ADK).")
    sys.exit(1)

def main():
    """Run an example travel agent interaction."""
    # Get user profile and itinerary info
    user_name = user_profile.get("name", "traveler")
    travel_dates = itinerary.get("travel_dates", {})
    
    print(f"Welcome to the Travel Agent Example, {user_name}!")
    
    if travel_dates:
        print(f"Your trip is scheduled from {travel_dates.get('start')} to {travel_dates.get('end')}.")
    
    print("\nYou can ask the travel agent about:")
    print("- Your itinerary")
    print("- Destinations")
    print("- Activities")
    print("- Travel recommendations")
    print("\nType 'exit' to quit.\n")
    
    while True:
        user_input = input("> ").strip()
        
        if user_input.lower() in ["exit", "quit"]:
            print("Thank you for using the Travel Agent. Safe travels!")
            break
        
        # Use the ADK agent to get a response
        response = travel_concierge_agent.generate_content(user_input)
        print(f"\n{response}\n")

if __name__ == "__main__":
    main() 