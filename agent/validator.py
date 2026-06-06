import re

# Dangerous SQL keywords
FORBIDDEN_KEYWORDS = {
    "DROP",
    "DELETE",
    "UPDATE",
    "INSERT",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "REPLACE",
    "RENAME",
    "ATTACH",
    "DETACH",
    "PRAGMA",
    "VACUUM",
    "GRANT",
    "REVOKE"
}


def remove_comments(sql: str) -> str:
    """
    Remove SQL comments before validation.
    """

    # Remove block comments
    sql = re.sub(
        r"/\*.*?\*/",
        "",
        sql,
        flags=re.DOTALL
    )

    # Remove inline comments
    sql = re.sub(
        r"--.*?$",
        "",
        sql,
        flags=re.MULTILINE
    )

    return sql.strip()


def remove_string_literals(sql: str) -> str:
    """
    Remove quoted strings to avoid false positives.
    """

    sql = re.sub(
        r"'[^']*'",
        "''",
        sql
    )

    sql = re.sub(
        r'"[^"]*"',
        '""',
        sql
    )

    return sql


def contains_multiple_statements(sql: str) -> bool:
    """
    Detect stacked SQL queries.
    """

    parts = [
        part.strip()
        for part in sql.split(";")
        if part.strip()
    ]

    return len(parts) > 1


def validate_sql(sql: str) -> bool:
    """
    Validate generated SQL.

    Returns:
        True  -> Safe
        False -> Unsafe
    """

    if not sql:
        return False

    sql = sql.strip()

    if len(sql) == 0:
        return False

    # Remove comments
    sql = remove_comments(sql)

    # Block stacked statements
    if contains_multiple_statements(sql):
        print(
            "Validation Error: Multiple SQL statements detected."
        )
        return False

    # Remove strings
    processed_sql = remove_string_literals(sql)

    processed_sql = processed_sql.upper()

    processed_sql = re.sub(
        r"\s+",
        " ",
        processed_sql
    )

    # Must start with SELECT or WITH
    if not (
        processed_sql.startswith("SELECT")
        or
        processed_sql.startswith("WITH")
    ):
        print(
            "Validation Error: Query must start with SELECT or WITH."
        )
        return False

    # Tokenize query
    tokens = set(
        re.findall(
            r"\b[A-Z_]+\b",
            processed_sql
        )
    )

    forbidden_found = (
        tokens.intersection(FORBIDDEN_KEYWORDS)
    )

    if forbidden_found:

        print(
            f"Validation Error: Forbidden keyword(s): {forbidden_found}"
        )

        return False

    return True


def validation_message(sql: str) -> str:
    """
    Human-readable validation result.
    """

    if validate_sql(sql):
        return "SQL validation passed."

    return "SQL validation failed."


if __name__ == "__main__":

    safe_queries = [

        "SELECT * FROM uploaded_data",

        """
        SELECT department,
               AVG(salary)
        FROM uploaded_data
        GROUP BY department
        """
    ]

    unsafe_queries = [

        "DROP TABLE uploaded_data",

        """
        SELECT * FROM uploaded_data;
        DROP TABLE uploaded_data;
        """,

        """
        UPDATE uploaded_data
        SET salary = 1000
        """
    ]

    print("\nSAFE TESTS\n")

    for query in safe_queries:

        print(query)
        print(
            "Result:",
            validate_sql(query)
        )
        print("-" * 50)

    print("\nUNSAFE TESTS\n")

    for query in unsafe_queries:

        print(query)
        print(
            "Result:",
            validate_sql(query)
        )
        print("-" * 50)