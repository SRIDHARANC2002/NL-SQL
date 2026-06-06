import sqlite3
import pandas as pd
import os


DB_PATH = "database/uploaded_data.db"
TABLE_NAME = "uploaded_data"


def create_database_from_dataframe(df: pd.DataFrame):
    """
    Creates SQLite database from uploaded dataframe.
    Existing table will be replaced.
    """

    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    try:
        df.to_sql(
            TABLE_NAME,
            conn,
            if_exists="replace",
            index=False
        )

        conn.commit()

    finally:
        conn.close()

    return DB_PATH, TABLE_NAME


def get_table_names():
    """
    Returns all non-system table names from the uploaded database.
    """

    if not os.path.exists(DB_PATH):
        return []

    conn = sqlite3.connect(DB_PATH)

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
        tables = cursor.fetchall()
        return [row[0] for row in tables]

    finally:
        conn.close()


def _get_primary_table():
    """
    Returns the main table to summarize.
    """

    tables = get_table_names()
    if not tables:
        return None
    return TABLE_NAME if TABLE_NAME in tables else tables[0]


def get_schema():
    """
    Returns schema information for the uploaded database.
    """

    tables = get_table_names()

    if not tables:
        return ""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    schema_parts = []

    try:
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            schema = f"Table: {table}\nColumns:\n"
            for col in columns:
                col_name = col[1]
                col_type = col[2]
                schema += f"- {col_name} ({col_type})\n"
            schema_parts.append(schema)

        return "\n".join(schema_parts)

    finally:
        conn.close()


def get_column_names():
    """
    Returns a list of column names for the active uploaded table.
    """

    if not os.path.exists(DB_PATH):
        return []

    table = _get_primary_table()
    if not table:
        return []

    conn = sqlite3.connect(DB_PATH)

    try:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        return [col[1] for col in columns]

    finally:
        conn.close()


def get_row_count():
    """
    Returns total row count for the primary uploaded table.
    """

    if not os.path.exists(DB_PATH):
        return 0

    table = _get_primary_table()
    if not table:
        return 0

    conn = sqlite3.connect(DB_PATH)

    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        return cursor.fetchone()[0]

    finally:
        conn.close()


def database_exists():
    return os.path.exists(DB_PATH)


if __name__ == "__main__":

    sample_df = pd.DataFrame(
        {
            "Department": ["IT", "HR", "Sales"],
            "Salary": [50000, 45000, 60000]
        }
    )

    create_database_from_dataframe(sample_df)

    print(get_schema())
    print(get_column_names())
    print(get_row_count())