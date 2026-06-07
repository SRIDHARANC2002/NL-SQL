import requests
import re

OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "llama3.2"

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL_NAME = "llama-3.3-70b-versatile"


def check_ollama_status():
    """
    Check whether Ollama is running and model exists.
    Returns:
        (is_running, has_model, models)
    """

    try:

        response = requests.get(
            f"{OLLAMA_URL}/api/tags",
            timeout=3
        )

        if response.status_code != 200:
            return False, False, []

        models_data = response.json().get("models", [])

        models = [
            model.get("name", "")
            for model in models_data
        ]

        has_model = any(
            MODEL_NAME in model.lower()
            for model in models
        )

        return True, has_model, models

    except Exception:
        return False, False, []


def clean_sql(response_text):
    """
    Extract SQL from model response.
    Removes markdown and extra text.
    """

    if not response_text:
        return ""

    code_match = re.search(
        r"```(?:sql)?(.*?)```",
        response_text,
        re.DOTALL | re.IGNORECASE
    )

    if code_match:
        sql = code_match.group(1)
    else:
        sql = response_text

    sql = sql.strip()

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")

    lines = []

    for line in sql.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith("--"):
            continue

        lines.append(line)

    sql = " ".join(lines)

    sql = re.sub(r"\s+", " ", sql)

    return sql.strip()


def generate_sql(question, schema, provider="ollama", api_key=None):
    """
    Convert natural language question to SQL using the chosen provider.
    """

    prompt = f"""
You are an expert SQLite SQL generator.

Your task is to convert the user's question into a valid SQLite query.

DATABASE SCHEMA:

{schema}

CRITICAL RULES FOR JOIN QUERIES:

1. ALWAYS verify which table each column belongs to BEFORE using it.
2. When using multiple tables, use table aliases (T1, T2, T3, etc).
3. In SELECT and GROUP BY, prefix each column with its table alias (e.g., T1.column_name, T3.column_name).
4. NEVER reference a column from the wrong table. Check schema carefully.
5. Verify JOIN conditions use columns that actually exist in those tables.
6. All columns in GROUP BY must match table ownership in schema.

GENERAL RULES:

1. Use ONLY columns present in schema.
2. Use appropriate tables from the schema (can be single or multiple tables with JOINs).
3. Return ONLY SQL.
4. Do not explain anything.
5. Do not use markdown.
6. Use SQLite syntax.
7. If aggregation is needed, use GROUP BY.
8. Use LIMIT for Top N queries.
9. Never generate INSERT, UPDATE, DELETE, DROP, ALTER.
10. Only generate SELECT queries.

Examples:

Question:
Show top 5 customers by revenue from completed orders

SQL:
SELECT 
    T3.customer_id,
    SUM(T1.unit_price * T2.quantity) AS total_revenue
FROM products AS T1
JOIN order_items AS T2 ON T1.product_id = T2.product_id
JOIN orders AS T3 ON T2.order_id = T3.order_id
WHERE T3.status = 'completed'
GROUP BY T3.customer_id
ORDER BY total_revenue DESC
LIMIT 5;

Question:
Show top 5 customers by revenue

SQL:
SELECT customer_id,
SUM(revenue) AS total_revenue
FROM uploaded_data
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 5;

Question:
Average salary by department

SQL:
SELECT department,
AVG(salary) AS avg_salary
FROM uploaded_data
GROUP BY department;

User Question:
{question}

SQL:
"""

    if provider == "groq":
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": GROQ_MODEL_NAME,
            "messages": [
                {"role": "system", "content": "You are a helpful data analyst AI that generates SQLite queries."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1,
            "top_p": 0.9
        }
        try:
            response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
            if response.status_code != 200:
                raise Exception(f"Groq API Error: {response.text}")
            raw_response = response.json()["choices"][0]["message"]["content"]
            sql = clean_sql(raw_response)
            return sql
        except Exception as e:
            raise Exception(f"SQL Generation Failed (Groq): {str(e)}")
            
    else:
        # Default to Ollama
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "top_p": 0.9
            }
        }
        try:
            response = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json=payload,
                timeout=60
            )
            if response.status_code != 200:
                raise Exception(
                    f"Ollama returned {response.status_code}"
                )
            raw_response = response.json().get("response", "")
            sql = clean_sql(raw_response)
            return sql
        except Exception as e:
            raise Exception(
                f"SQL Generation Failed (Ollama): {str(e)}"
            )

def agent_loop_generate_and_run(question, schema, execute_func, validate_func, provider="ollama", api_key=None, max_retries=3):
    """
    Agent loop that generates SQL, validates, executes, and retries on failure.
    """
    prompt = f"Generate a valid SQLite SELECT query for this schema:\n{schema}\n\nQuestion: {question}\nReturn ONLY the SQL code."
    
    messages = [
        {"role": "system", "content": "You are a helpful data analyst AI that generates SQLite queries."},
        {"role": "user", "content": prompt}
    ]
    
    last_error = None
    last_sql = ""

    for attempt in range(max_retries):
        try:
            if provider == "groq":
                headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
                payload = {"model": GROQ_MODEL_NAME, "messages": messages, "temperature": 0.1}
                response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
                if response.status_code != 200:
                    raise Exception(f"Groq API Error: {response.text}")
                raw_response = response.json()["choices"][0]["message"]["content"]
            else:
                # Format messages array to plain string for Ollama prompt
                ollama_prompt = "\n".join([m["content"] for m in messages])
                payload = {"model": MODEL_NAME, "prompt": ollama_prompt, "stream": False, "options": {"temperature": 0.1}}
                response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=60)
                if response.status_code != 200:
                    raise Exception(f"Ollama returned {response.status_code}")
                raw_response = response.json().get("response", "")

            sql = clean_sql(raw_response)
            last_sql = sql
            
            # 1. Validate SQL
            is_valid = validate_func(sql)
            if not is_valid:
                error_msg = f"The generated SQL '{sql}' is invalid. It might contain restricted keywords. Please generate a simple SELECT query."
                messages.append({"role": "assistant", "content": raw_response})
                messages.append({"role": "user", "content": error_msg})
                last_error = error_msg
                continue
                
            # 2. Execute SQL
            results_df = execute_func(sql)
            return sql, results_df
            
        except Exception as e:
            error_msg = f"Execution failed with error: {str(e)}. Please correct the SQL query and return ONLY the corrected SQL code."
            # Avoid referencing undefined variable if first request fails
            messages.append({"role": "assistant", "content": raw_response if 'raw_response' in locals() else last_sql})
            messages.append({"role": "user", "content": error_msg})
            last_error = str(e)
            
    raise Exception(f"Agent Loop Failed after {max_retries} retries. Last Error: {last_error}\nLast SQL attempted: {last_sql}")

if __name__ == "__main__":

    schema = """
Table: uploaded_data

Columns:
- customer_id (TEXT)
- revenue (REAL)
- gender (TEXT)
- age (INTEGER)
"""

    question = "Top 5 customers by revenue"

    print("Checking Ollama...")

    status = check_ollama_status()

    print(status)

    if status[0]:

        sql = generate_sql(
            question,
            schema
        )

        print("\nGenerated SQL:\n")
        print(sql)