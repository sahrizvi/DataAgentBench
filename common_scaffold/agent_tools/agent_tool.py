from common_scaffold.db_utils.loader import query_db

def execute_agent_query(tool_args: dict):
    """
    Unified interface for agent queries.

    Args:
        tool_args (dict): A dictionary of query parameters. Example:
            {
                "db_type": "sqlite",
                "db_path": "data/mydb.sqlite",
                "sql": "SELECT * FROM my_table"
            }

    Returns:
        pandas.DataFrame: The query result as a DataFrame.
    """
    df = query_db(**tool_args)
    print(f"[AgentTool] Query executed: fetched {len(df)} rows.")
    return df
