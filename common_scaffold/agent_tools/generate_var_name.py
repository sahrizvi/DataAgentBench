from uuid import uuid4

def generate_var_name(tool_name: str, tool_args: dict, step: int | None = None) -> str:
    """
    Generate a unique variable name for a given tool call.

    Args:
        tool_name (str): Name of the tool (query_db, list_dbs, execute_python, etc.)
        tool_args (dict): Arguments passed to the tool.
        step (int, optional): Current step in the agent loop, for traceability.

    Returns:
        str: Generated variable name.
    """
    if tool_name == "query_db":
        db_name = tool_args.get("db_name", "").lower()
        sql_or_query = tool_args.get("sql", "") or tool_args.get("query", "")

        # SQL
        if tool_args.get("db_type") in {"mysql", "sqlite", "duckdb"} or \
           (isinstance(sql_or_query, str) and sql_or_query.strip().lower().startswith(("select", "with"))):
            sql = sql_or_query.lower()
            if "from" in sql:
                table = sql.split("from")[1].split()[0].strip("`").strip()
                if step is not None:
                    return f"df_{table}_step{step}"
                else:
                    return f"df_{table}_{uuid4().hex[:6]}"
            else:
                return f"df_result_{uuid4().hex[:6]}"

        # MongoDB
        elif tool_args.get("db_type") == "mongo":
            collection = tool_args.get("collection")
            if collection:
                if step is not None:
                    return f"df_{collection}_step{step}"
                else:
                    return f"df_{collection}_{uuid4().hex[:6]}"
            else:
                return f"df_mongo_result_{uuid4().hex[:6]}"

        else:
            return f"df_result_{uuid4().hex[:6]}"

    elif tool_name == "list_dbs":
        db_name = tool_args.get("db_name", "").lower()
        if step is not None:
            return f"tables_{db_name}_step{step}"
        else:
            return f"tables_{db_name}_{uuid4().hex[:6]}"

    elif tool_name == "execute_python":
        if step is not None:
            return f"exec_result_step{step}"
        else:
            return f"exec_result_{uuid4().hex[:6]}"

    else:
        return f"result_{uuid4().hex[:6]}"
