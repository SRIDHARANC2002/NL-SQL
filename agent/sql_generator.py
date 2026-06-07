import requests
import re

# Configuration
OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "llama3.2"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL_NAME = "llama-3.3-70b-versatile"


def check_ollama_status():
    """Check whether Ollama is running and the required model exists.

    Returns:
        tuple: (is_running: bool, has_model: bool, models: list)
    """
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        if response.status_code != 200:
            return False, False, []
        models_data = response.json().get("models", [])
        models = [model.get("name", "") for model in models_data]
        has_model = any(MODEL_NAME.lower() in model.lower() for model in models)
        return True, has_model, models
    except Exception:
        return False, False, []


def clean_sql(response_text: str) -> str:
    """Extract raw SQL from a model response, stripping markdown and comments.
    """
    if not response_text:
        return ""
    # Grab code block if present
    code_match = re.search(r"```(?:sql)?(.*?)```", response_text, re.DOTALL | re.IGNORECASE)
    sql = code_match.group(1) if code_match else response_text
    # Remove any stray markdown fences
    sql = sql.replace("```sql", "").replace("```", "")
    # Strip leading/trailing whitespace and collapse lines
    lines = []
    for line in sql.splitlines():
        line = line.strip()
        if not line or line.startswith("--"):
            continue
        lines.append(line)
    cleaned = " ".join(lines)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def generate_sql(question: str, schema: str, provider: str = "ollama", api_key: str | None = None) -> str:
    """Generate SQL from a natural‑language question.

    Args:
        question: User's question.
        schema: Database schema description.
        provider: "ollama" or "groq".
        api_key: Required when provider is "groq".
    """
    prompt = f"""
You are an expert SQLite SQL generator.

DATABASE SCHEMA:
{schema}

Question: {question}

Return ONLY the SQL query without any explanations or markdown.
"""
    if provider == "groq":
        if not api_key:
            raise ValueError("Groq API key is required for Groq provider")
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": GROQ_MODEL_NAME,
            "messages": [
                {"role": "system", "content": "You are a helpful data analyst AI that generates SQLite queries."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1,
            "top_p": 0.9
        }
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        if response.status_code != 200:
            raise Exception(f"Groq API Error: {response.text}")
        raw = response.json()["choices"][0]["message"]["content"]
        return clean_sql(raw)
    else:  # Ollama
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.1, "top_p": 0.9}
        }
        response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=60)
        if response.status_code != 200:
            raise Exception(f"Ollama returned {response.status_code}")
        raw = response.json().get("response", "")
        return clean_sql(raw)


if __name__ == "__main__":
    sample_schema = """
Table: uploaded_data
Columns:
- customer_id (TEXT)
- revenue (REAL)
- gender (TEXT)
- age (INTEGER)
"""
    sample_question = "Top 5 customers by revenue"
    print("Checking Ollama status...")
    status = check_ollama_status()
    print(status)
    if status[0] and status[1]:
        sql = generate_sql(sample_question, sample_schema)
        print("\nGenerated SQL:\n", sql)
    else:
        print("Ollama not ready – cannot generate SQL.")
