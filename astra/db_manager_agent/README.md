# Async SQLite Tools for Agent Development Kit

This module provides asynchronous SQLite database tools for use with the Google Agent Development Kit (ADK).

## Features

- Async SQLite operations using aiosqlite
- Integration with ADK's ToolContext for state management
- Database connection pooling with singleton instance
- Error handling and standardized response format
- Tools for common database operations:
  - Reading data (SELECT queries)
  - Writing data (INSERT, UPDATE, DELETE)
  - Creating tables
  - Listing tables
  - Describing table schemas
  - Setting database path

## Installation

1. Make sure to install the required packages:

```bash
pip install -r requirements.txt
```

2. Import the tools in your agent code

## Usage

Here's a simple example of how to use these tools:

```python
import asyncio
from google.adk.tools.tool_context import ToolContext
from astra.db_manager_agent.sqlite_tools import (
    set_db_path, 
    create_table, 
    write_query, 
    read_query
)

async def example():
    # Create a tool context
    tool_context = ToolContext()
    
    # Set database path
    await set_db_path("my_database.db", tool_context)
    
    # Create a table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
    """
    await create_table(create_table_sql, tool_context)
    
    # Insert data
    insert_sql = """
    INSERT INTO products (name, price) VALUES 
    ('Widget', 19.99),
    ('Gadget', 24.99)
    """
    await write_query(insert_sql, tool_context)
    
    # Query data
    select_sql = "SELECT * FROM products WHERE price < 25.0"
    result = await read_query(select_sql, tool_context)
    print(result)
```

## Response Format

All tools return a dictionary with at least a `status` field, which is either "success" or "error". 

For successful operations:
- `read_query` returns a `data` field with query results
- `list_tables` returns a `tables` field with all table names
- `describe_table` returns a `schema` field with table structure
- `write_query` returns `affected_rows` with the count of modified rows

For error conditions, all tools return an `error_message` field with details.

## Running the Example

An example script is provided in the `examples` directory:

```bash
python -m astra.db_manager_agent.examples.sqlite_example
```

## Integration with ADK

When integrating with ADK, you can register these functions as tools for your agent with proper asynchronous handling. 