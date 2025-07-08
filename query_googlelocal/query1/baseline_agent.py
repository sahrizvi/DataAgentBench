import sys
import pandas as pd
from pathlib import Path

# Add common_scaffold to Python path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from common_scaffold.agent_tools.agent_tool import execute_agent_query
from common_scaffold.db_utils.mysql_importer import ensure_mysql_data


def main():
    # === Step 1: Ensure MySQL database is initialized ===
    ensure_mysql_data(
        db_name="googlelocal_db",
        sql_file="../query_dataset/business_description.sql"
    )

    # Set pandas display options
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 200)
    pd.set_option('display.max_rows', 20)

    # === Step 2: Query MySQL ===
    print("\n=== Querying MySQL Tables ===")
    mysql_args = {
        "db_type": "mysql",
        "db": "googlelocal_db",
        "sql": "SHOW TABLES;"
    }
    df_mysql = execute_agent_query(mysql_args)
    print(df_mysql)

    # Preview each MySQL table
    for table in df_mysql.iloc[:, 0]:  # first column is table name
        print(f"\n=== Preview of MySQL table: {table} ===")
        sample_query = {
            "db_type": "mysql",
            "db": "googlelocal_db",
            "sql": f"SELECT * FROM {table} LIMIT 5;"
        }
        df_sample = execute_agent_query(sample_query)
        print(df_sample)

    # === Step 3: Query SQLite ===
    print("\n=== Querying SQLite Tables ===")
    sqlite_args = {
        "db_type": "sqlite",
        "db_path": "../query_dataset/review_query.db",
        "sql": "SELECT name FROM sqlite_master WHERE type='table';"
    }
    df_sqlite = execute_agent_query(sqlite_args)
    print(df_sqlite)

    # Preview each SQLite table
    for table in df_sqlite["name"]:
        print(f"\n=== Preview of SQLite table: {table} ===")
        sample_query = {
            "db_type": "sqlite",
            "db_path": "../query_dataset/review_query.db",
            "sql": f"SELECT * FROM {table} LIMIT 5;"
        }
        df_sample = execute_agent_query(sample_query)
        print(df_sample)


if __name__ == "__main__":
    main()
