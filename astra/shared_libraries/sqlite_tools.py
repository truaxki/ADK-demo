import os
import sqlite3
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
from contextlib import closing
from google.adk.tools.tool_context import ToolContext

logger = logging.getLogger('astra_sqlite_tools')

class SqliteDatabase:
    def __init__(self, db_path: str):
        self.db_path = str(Path(db_path).expanduser())
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

    def _init_database(self):
        """Initialize connection to the SQLite database"""
        logger.debug("Initializing database connection")
        with closing(sqlite3.connect(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            conn.close()

    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute a SQL query synchronously and return results as a list of dictionaries"""
        logger.debug(f"Executing query: {query}")
        try:
            with closing(sqlite3.connect(self.db_path)) as conn:
                conn.row_factory = sqlite3.Row
                with closing(conn.cursor()) as cursor:
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)

                    if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 'ALTER')):
                        conn.commit()
                        affected = cursor.rowcount
                        logger.debug(f"Write query affected {affected} rows")
                        return [{"affected_rows": affected}]

                    results = [dict(row) for row in cursor.fetchall()]
                    logger.debug(f"Read query returned {len(results)} rows")
                    return results
        except Exception as e:
            logger.error(f"Database error executing query: {e}")
            raise

# Create a single instance that can be imported and reused
_db_instance = None

def get_db_instance(db_path: str = "sqlite_db.db") -> SqliteDatabase:
    """Get or create the database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = SqliteDatabase(db_path)
    return _db_instance

def set_db_path(db_path: str, tool_context: ToolContext) -> dict:
    """Set the SQLite database path in the session state.
    
    Args:
        db_path (str): Path to the SQLite database file
        tool_context (ToolContext): Context to store the database path
        
    Returns:
        dict: Status of the operation
    """
    try:
        # Validate input
        if not db_path:
            return {
                "status": "error",
                "error_message": "Database path cannot be empty"
            }
            
        # Handle both absolute and relative paths
        if os.path.isabs(db_path):
            full_path = db_path
        else:
            # If path starts with a directory like "data/", ensure the directory exists
            if os.path.dirname(db_path):
                try:
                    os.makedirs(os.path.dirname(db_path), exist_ok=True)
                    logger.info(f"Created directory: {os.path.dirname(db_path)}")
                except Exception as e:
                    logger.error(f"Failed to create directory {os.path.dirname(db_path)}: {str(e)}")
                    return {
                        "status": "error",
                        "error_message": f"Failed to create directory: {str(e)}"
                    }
            
            # Resolve to absolute path
            full_path = os.path.abspath(db_path)
        
        # Create parent directories if needed
        try:
            Path(os.path.dirname(full_path)).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"Failed to create parent directories for {full_path}: {str(e)}")
            return {
                "status": "error",
                "error_message": f"Failed to create parent directories: {str(e)}"
            }
        
        # Store the path in context state
        tool_context.state["sqlite_db_path"] = full_path
        
        # Initialize the database
        try:
            db_instance = get_db_instance(full_path)
            
            # Verify database is accessible by executing a simple query
            with closing(sqlite3.connect(full_path)) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.close()
                
            logger.info(f"Database successfully initialized at {full_path}")
        except Exception as e:
            logger.error(f"Failed to initialize database at {full_path}: {str(e)}")
            return {
                "status": "error",
                "error_message": f"Failed to initialize database: {str(e)}"
            }
        
        # Log the actual path for debugging
        working_dir = os.getcwd()
        logger.info(f"Database path set to: {full_path} (working dir: {working_dir})")
        print(f"Database path set to: {full_path} (working dir: {working_dir})")
        
        return {
            "status": "success",
            "message": f"Database path set to {full_path}",
            "absolute_path": full_path,
            "working_directory": working_dir
        }
    except Exception as e:
        logger.error(f"Unexpected error in set_db_path: {str(e)}")
        return {
            "status": "error",
            "error_message": f"Error setting database path: {str(e)}"
        }

def create_database(db_path: str, tool_context: ToolContext) -> dict:
    """Create a new SQLite database at the specified path.
    
    This is a convenience function that calls set_db_path with a more explicit name
    to make it clear that a new database will be created if it doesn't exist.
    
    Args:
        db_path (str): Path where the new SQLite database should be created
        tool_context (ToolContext): Context to store the database path
        
    Returns:
        dict: Status of the operation
    """
    logger.info(f"Creating database at path: {db_path}")
    print(f"Creating database at path: {db_path}")
    
    # Validate input
    if not db_path:
        return {
            "status": "error",
            "error_message": "Database path cannot be empty"
        }
    
    # Handle directory creation for paths with directories
    if os.path.dirname(db_path):
        try:
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            logger.info(f"Created directory: {os.path.dirname(db_path)}")
        except Exception as e:
            logger.error(f"Failed to create directory {os.path.dirname(db_path)}: {str(e)}")
            return {
                "status": "error",
                "error_message": f"Failed to create directory: {str(e)}"
            }
    
    # Call set_db_path to create the database
    result = set_db_path(db_path, tool_context)
    
    if result["status"] == "success":
        # Verify the database was actually created
        full_path = result["absolute_path"]
        if os.path.exists(full_path):
            # Try to open and perform a simple operation to verify it's a valid SQLite database
            try:
                with closing(sqlite3.connect(full_path)) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT sqlite_version()")
                    version = cursor.fetchone()[0]
                    cursor.close()
                    
                logger.info(f"Database created successfully at {full_path} (SQLite version: {version})")
                print(f"Database created successfully at {full_path} (SQLite version: {version})")
                
                result["message"] = f"Database created at {full_path}"
                result["sqlite_version"] = version
            except Exception as e:
                logger.error(f"Database file exists but cannot be opened as SQLite database: {str(e)}")
                return {
                    "status": "error",
                    "error_message": f"Database file exists but cannot be opened: {str(e)}",
                    "file_path": full_path
                }
        else:
            logger.error(f"Database file was not created at {full_path}")
            return {
                "status": "error",
                "error_message": f"Database file was not created at {full_path}",
                "attempted_path": full_path,
                "working_directory": os.getcwd()
            }
    
    return result

def create_table(query: str, tool_context: ToolContext) -> dict:
    """Create a new table in the SQLite database.
    
    Args:
        query (str): CREATE TABLE SQL statement
        tool_context (ToolContext): Context with database configuration
        
    Returns:
        dict: Operation result with status
    """
    # Get the database path from context or use default
    db_path = tool_context.state.get("sqlite_db_path", "sqlite_db.db")
    db = get_db_instance(db_path)
    
    try:
        # Validate that this is a CREATE TABLE query
        if not query.strip().upper().startswith("CREATE TABLE"):
            return {
                "status": "error",
                "error_message": "Only CREATE TABLE statements are allowed"
            }
        
        # Execute the query
        db.execute_query(query)
        
        # Return success
        return {
            "status": "success",
            "message": "Table created successfully"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Database error: {str(e)}"
        }

def write_query(query: str, tool_context: ToolContext) -> dict:
    """Execute an INSERT, UPDATE, or DELETE query on the SQLite database.
    
    Args:
        query (str): SQL query to execute
        tool_context (ToolContext): Context with database configuration
        
    Returns:
        dict: Operation result with status and affected rows
    """
    # Get the database path from context or use default
    db_path = tool_context.state.get("sqlite_db_path", "sqlite_db.db")
    db = get_db_instance(db_path)
    
    try:
        # Validate that this is NOT a SELECT query
        if query.strip().upper().startswith("SELECT"):
            return {
                "status": "error",
                "error_message": "SELECT queries are not allowed for write_query"
            }
        
        # Execute the query
        result = db.execute_query(query)
        
        # Return the result
        return {
            "status": "success",
            "affected_rows": result[0].get("affected_rows", 0)
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Database error: {str(e)}"
        }

def read_query(query: str, tool_context: ToolContext) -> dict:
    """Execute a SELECT query on the SQLite database.
    
    Args:
        query (str): SELECT SQL query to execute
        tool_context (ToolContext): Context with database configuration
        
    Returns:
        dict: Query results with status and data
    """
    # Get the database path from context or use default
    db_path = tool_context.state.get("sqlite_db_path", "sqlite_db.db")
    db = get_db_instance(db_path)
    
    try:
        # Validate that this is a SELECT query
        if not query.strip().upper().startswith("SELECT"):
            return {
                "status": "error",
                "error_message": "Only SELECT queries are allowed for read_query"
            }
        
        # Execute the query
        results = db.execute_query(query)
        
        # Return the results
        return {
            "status": "success",
            "data": results
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Database error: {str(e)}"
        }

def list_tables(tool_context: ToolContext) -> dict:
    """List all tables in the SQLite database.
    
    Args:
        tool_context (ToolContext): Context with database configuration
        
    Returns:
        dict: List of tables with status
    """
    # Get the database path from context or use default
    db_path = tool_context.state.get("sqlite_db_path", "sqlite_db.db")
    db = get_db_instance(db_path)
    
    try:
        # Execute the query to list tables
        results = db.execute_query(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        
        # Extract table names from results
        tables = [row.get("name") for row in results if row.get("name") != "sqlite_sequence"]
        
        # Return the table list
        return {
            "status": "success",
            "tables": tables
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Database error: {str(e)}"
        }

def describe_table(table_name: str, tool_context: ToolContext) -> dict:
    """Get the schema information for a specific table.
    
    Args:
        table_name (str): Name of the table to describe
        tool_context (ToolContext): Context with database configuration
        
    Returns:
        dict: Table schema with status
    """
    # Get the database path from context or use default
    db_path = tool_context.state.get("sqlite_db_path", "sqlite_db.db")
    db = get_db_instance(db_path)
    
    try:
        # Execute the query to get table schema
        results = db.execute_query(f"PRAGMA table_info({table_name})")
        
        # If no results, table might not exist
        if not results:
            return {
                "status": "error",
                "error_message": f"Table '{table_name}' does not exist"
            }
        
        # Return the schema information
        return {
            "status": "success",
            "schema": results
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Database error: {str(e)}"
        } 