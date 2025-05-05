"""Database Manager Agent for Astra.

This agent provides database schema design and management capabilities.
"""

import os
import json
from pathlib import Path
from datetime import datetime

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# Import prompt instructions
from .prompt import DB_MANAGER_INSTR

# Define model
MODEL_GPT_4O_MINI = "openai/gpt-4o-mini"

# Load environment variables from .env
try:
    from dotenv import load_dotenv
    load_dotenv()
    # Override model if specified
    MODEL = os.getenv("ASTRA_DB_MANAGER_MODEL", MODEL_GPT_4O_MINI)
except ImportError:
    MODEL = MODEL_GPT_4O_MINI

def load_database_catalog():
    """Load database catalog from databases.json."""
    catalog_path = Path(__file__).parent / "databases.json"
    try:
        with open(catalog_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return default empty catalog if file not found
        return {
            "database_catalog": {
                "version": "1.0",
                "last_updated": datetime.now().strftime("%Y-%m-%d"),
                "databases": []
            }
        }

# Get data for prompt
database_catalog = load_database_catalog().get("database_catalog", {})
# Always use the current time
current_time = datetime.now().isoformat()

# Initialize the Database Manager agent
db_manager_agent = Agent(
    name="db_manager_agent",
    model=LiteLlm(model=MODEL),
    description="A specialized agent that helps design and manage database schemas for various projects.",
    instruction=DB_MANAGER_INSTR.format(
        database_catalog=json.dumps(database_catalog, indent=2),
        _time=current_time
    ),
    tools=[],  # No tools for now, as specified by the user
)

print(f"✅ Agent '{db_manager_agent.name}' created using model '{MODEL}'.") 