from sqlalchemy import create_engine
import pandas as pd
from common_scaffold import config


def mysql_query(sql: str, db: str = None) -> pd.DataFrame:
    """
    Execute a MySQL query and return result as a pandas DataFrame.
    Uses SQLAlchemy for better compatibility.

    Args:
        sql (str): SQL query to execute
        db (str): Database name. If None, use config.MYSQL_DB

    Returns:
        pd.DataFrame: Query result
    """
    db = db or config.MYSQL_DB

    # Build SQLAlchemy connection string
    uri = (
        f"mysql+mysqlconnector://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}"
        f"@{config.MYSQL_HOST}:{config.MYSQL_PORT}/{db}"
    )
    engine = create_engine(uri)

    # Execute query and return DataFrame
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn)

    return df
