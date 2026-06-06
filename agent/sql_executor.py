import sqlite3
import pandas as pd
import os

DB_PATH = "database/uploaded_data.db"


def execute_sql(sql: str) -> pd.DataFrame:
    """
    Execute SQL query and return results as DataFrame.

    Parameters:
        sql (str): Valid SQL query

    Returns:
        pd.DataFrame
    """

    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}"
        )

    conn = None

    try:

        conn = sqlite3.connect(DB_PATH)

        df = pd.read_sql_query(
            sql,
            conn
        )

        return df

    except Exception as e:

        raise Exception(
            f"SQL Execution Error: {str(e)}"
        )

    finally:

        if conn:
            conn.close()


def get_table_preview(limit: int = 10):
    """
    Preview uploaded dataset.
    """

    query = f"""
    SELECT *
    FROM uploaded_data
    LIMIT {limit}
    """

    return execute_sql(query)


def get_total_rows():
    """
    Get total rows in uploaded table.
    """

    conn = None

    try:

        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM uploaded_data
            """
        )

        count = cursor.fetchone()[0]

        return count

    finally:

        if conn:
            conn.close()


def get_column_names():
    """
    Get all column names.
    """

    conn = None

    try:

        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()

        cursor.execute(
            """
            PRAGMA table_info(uploaded_data)
            """
        )

        columns = cursor.fetchall()

        return [
            col[1]
            for col in columns
        ]

    finally:

        if conn:
            conn.close()


def get_table_info():
    """
    Return schema information.
    """

    conn = None

    try:

        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()

        cursor.execute(
            """
            PRAGMA table_info(uploaded_data)
            """
        )

        columns = cursor.fetchall()

        schema = []

        for col in columns:

            schema.append(
                {
                    "column_name": col[1],
                    "data_type": col[2]
                }
            )

        return pd.DataFrame(schema)

    finally:

        if conn:
            conn.close()


if __name__ == "__main__":

    try:

        print("\nRows in Dataset:")
        print(get_total_rows())

        print("\nColumns:")
        print(get_column_names())

        print("\nSchema:")
        print(get_table_info())

        print("\nPreview:")
        print(get_table_preview())

        query = """
        SELECT *
        FROM uploaded_data
        LIMIT 5
        """

        result = execute_sql(query)

        print("\nQuery Result:")
        print(result)

    except Exception as e:

        print(f"Error: {e}")