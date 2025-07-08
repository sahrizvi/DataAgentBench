import sys
from pathlib import Path

# 加入 common_scaffold
sys.path.append(str(Path(__file__).resolve().parents[2]))

from common_scaffold.agent_tools.agent_tool import execute_agent_query

def main():
    print("\n=== Testing MySQL ===")
    mysql_args = {
        "db_type": "mysql",
        "sql": "SHOW TABLES;"
    }
    df_mysql = execute_agent_query(mysql_args)
    print(df_mysql)

    print("\n=== Testing SQLite ===")
    sqlite_args = {
        "db_type": "sqlite",
        "db_path": "../query_dataset/review_query.db",
        "sql": "SELECT name FROM sqlite_master WHERE type='table';"
    }
    df_sqlite = execute_agent_query(sqlite_args)
    print(df_sqlite)

if __name__ == "__main__":
    main()
