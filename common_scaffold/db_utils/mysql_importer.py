import mysql.connector
from pathlib import Path
from common_scaffold import config
import re


def database_exists(db_name: str) -> bool:
    """
    Check if a database exists on the MySQL server.
    """
    conn = mysql.connector.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        port=config.MYSQL_PORT
    )
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES;")
    dbs = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return db_name in dbs


def database_has_tables(db_name: str) -> bool:
    """
    Check if a database has at least one table.
    """
    conn = mysql.connector.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        port=config.MYSQL_PORT,
        database=db_name
    )
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    cursor.close()
    conn.close()
    return len(tables) > 0


def import_sql_to_mysql(sql_file: str, db_name: str):
    """
    Import a .sql file into the specified MySQL database.
    """
    conn = mysql.connector.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        port=config.MYSQL_PORT
    )
    cursor = conn.cursor()

    # Create database if not exists and use it
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cursor.execute(f"USE {db_name}")

    # Read SQL file
    sql_text = Path(sql_file).read_text(encoding="utf-8")

    # Replace any existing USE statements in the SQL file
    sql_text = re.sub(r"USE\s+\w+;", f"USE {db_name};", sql_text, flags=re.IGNORECASE)

    # Execute statements one by one
    statements = sql_text.split(';')
    for statement in statements:
        stmt = statement.strip()
        if stmt:
            try:
                print(f"▶️ Executing: {stmt[:60]}...")
                cursor.execute(stmt)
            except mysql.connector.Error as err:
                print(f"⚠️ Error: {err}")

    conn.commit()
    cursor.close()
    conn.close()
    print(f"🎉 SQL file '{sql_file}' imported into database '{db_name}'.")


def ensure_mysql_data(db_name: str, sql_file: str):
    """
    Ensure that the MySQL database exists and has at least one table.
    If not, import data from the provided SQL file.

    Args:
        db_name (str): Target database name
        sql_file (str): Path to the .sql file
    """
    if not database_exists(db_name):
        print(f"⚠️ Database '{db_name}' not found. Importing from '{sql_file}'...")
        import_sql_to_mysql(sql_file, db_name)
    elif not database_has_tables(db_name):
        print(f"⚠️ Database '{db_name}' is empty. Importing from '{sql_file}'...")
        import_sql_to_mysql(sql_file, db_name)
    else:
        print(f"✅ Database '{db_name}' already exists and has tables. No action needed.")
