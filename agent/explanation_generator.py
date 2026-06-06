import requests
import re

OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "llama3.2"


def fallback_explanation(sql: str):
    """
    Basic fallback explanation when Ollama is unavailable.
    """

    sql_lower = sql.lower()

    if "group by" in sql_lower:
        return (
            "This query groups the dataset and "
            "calculates summary statistics for each group."
        )

    if "avg(" in sql_lower:
        return (
            "This query calculates an average value "
            "from the uploaded dataset."
        )

    if "sum(" in sql_lower:
        return (
            "This query calculates total values "
            "from the uploaded dataset."
        )

    if "count(" in sql_lower:
        return (
            "This query counts records in the uploaded dataset."
        )

    return (
        "This query retrieves information from "
        "the uploaded dataset."
    )


def clean_response(text: str):
    """
    Clean model output.
    """

    if not text:
        return ""

    text = text.replace("```", "")
    text = text.replace("sql", "")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def explain_sql(sql: str):
    """
    Generate business explanation for SQL query.
    """

    prompt = f"""
You are a senior business analyst.

Explain the SQL query in plain English.

Rules:

1. Maximum 2 sentences.
2. Business-friendly language.
3. Do not mention SQL syntax.
4. Do not mention SELECT, GROUP BY, ORDER BY.
5. Explain what insight the user receives.
6. Keep explanation short and clear.

SQL Query:

{sql}

Explanation:
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2
        }
    }

    try:

        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            return fallback_explanation(sql)

        explanation = (
            response.json()
            .get("response", "")
            .strip()
        )

        explanation = clean_response(explanation)

        if not explanation:
            return fallback_explanation(sql)

        return explanation

    except Exception:

        return fallback_explanation(sql)


if __name__ == "__main__":

    sample_sql = """
    SELECT department,
           AVG(salary)
    FROM uploaded_data
    GROUP BY department
    """

    print(
        explain_sql(sample_sql)
    )