import requests
import re
from agent.sql_generator import clean_sql

OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "llama3.2"

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL_NAME = "llama-3.3-70b-versatile"

def agent_loop_generate_and_run(question, schema, execute_func, validate_func, provider="ollama", api_key=None, max_retries=3):
    """
    Agent loop that generates SQL, validates, executes, and retries on failure.
    Extracted to a separate file to prevent IDE undo conflicts.
    """
    prompt = f"Generate a valid SQLite SELECT query for this schema:\n{schema}\n\nQuestion: {question}\nReturn ONLY the SQL code."
    
    messages = [
        {"role": "system", "content": "You are a helpful data analyst AI that generates SQLite queries."},
        {"role": "user", "content": prompt}
    ]
    
    last_error = None
    last_sql = ""

    print(f"\n🚀 [Agent Loop] Starting with Provider: {provider.upper()}")
    print(f"🚀 [Agent Loop] Max Retries: {max_retries}")

    for attempt in range(max_retries):
        current_attempt = attempt + 1
        print(f"\n🔄 [Agent Loop] Attempt {current_attempt}/{max_retries}...")
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
                ollama_prompt = "\\n".join([m["content"] for m in messages])
                payload = {"model": MODEL_NAME, "prompt": ollama_prompt, "stream": False, "options": {"temperature": 0.1}}
                response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=60)
                if response.status_code != 200:
                    raise Exception(f"Ollama returned {response.status_code}")
                raw_response = response.json().get("response", "")

            sql = clean_sql(raw_response)
            last_sql = sql
            
            # 1. Validate SQL
            print(f"⚙️ [Agent Loop] Validating generated SQL...")
            is_valid = validate_func(sql)
            if not is_valid:
                error_msg = f"The generated SQL '{sql}' is invalid. It might contain restricted keywords. Please generate a simple SELECT query."
                print(f"❌ [Agent Loop] Validation Failed: {error_msg}")
                messages.append({"role": "assistant", "content": raw_response})
                messages.append({"role": "user", "content": error_msg})
                last_error = error_msg
                print(f"🔄 [Agent Loop] Triggering Retry...")
                continue
                
            # 2. Execute SQL
            print(f"⚙️ [Agent Loop] Validation Passed. Executing SQL...")
            results_df = execute_func(sql)
            print(f"✅ [Agent Loop] SQL executed successfully on Attempt {current_attempt}!")
            return sql, results_df
            
        except Exception as e:
            error_msg = f"Execution failed with error: {str(e)}. Please correct the SQL query and return ONLY the corrected SQL code."
            print(f"❌ [Agent Loop] Execution Failed: {str(e)}")
            messages.append({"role": "assistant", "content": raw_response if 'raw_response' in locals() else last_sql})
            messages.append({"role": "user", "content": error_msg})
            last_error = str(e)
            print(f"🔄 [Agent Loop] Triggering Retry...")
            
    print(f"🚨 [Agent Loop] All {max_retries} retries exhausted. Failing.")
    raise Exception(f"Agent Loop Failed after {max_retries} retries. Last Error: {last_error}\nLast SQL attempted: {last_sql}")
