"""
Test importing sqlite_tools from the new location.
"""

try:
    from shared_libraries.sqlite_tools import (
        set_db_path,
        create_database,
        create_table,
        write_query,
        read_query,
        list_tables,
        describe_table
    )
    print("✅ Successfully imported from shared_libraries.sqlite_tools")
except ImportError as e:
    print(f"❌ Error importing from shared_libraries.sqlite_tools: {e}")

try:
    from astra.shared_libraries.sqlite_tools import (
        set_db_path,
        create_database,
        create_table,
        write_query,
        read_query,
        list_tables,
        describe_table
    )
    print("✅ Successfully imported from astra.shared_libraries.sqlite_tools")
except ImportError as e:
    print(f"❌ Error importing from astra.shared_libraries.sqlite_tools: {e}")

try:
    from db_manager_agent.agent import db_manager_agent
    print("✅ Successfully imported db_manager_agent")
except ImportError as e:
    print(f"❌ Error importing db_manager_agent: {e}")

print("\nTest completed.") 