# AI Usage & Prompt Engineering Note

This document summarizes how AI is incorporated into the **NL-To-SQL Analytics Agent**, the prompt engineering design, local LLM challenges encountered, and future improvement paths.

---

## 1. Role of AI

A local Large Language Model (**Ollama llama3.2**) powers two core tasks:

1. **Natural Language → SQL** (`agent/sql_generator.py`): Converts plain English questions into valid SQLite queries against the `retail_sales` and `sales` tables.
2. **SQL Explanation** (`agent/explanation_generator.py`): Translates generated SQL logic into plain business language for non-technical users.

When Ollama is offline or `llama3.2` is not pulled, both tasks automatically fall back to a rule-based engine with no user-facing disruption.

---

## 2. Prompt Engineering Approach

### SQL Generation Prompt Structure

```text
You are a SQLite database expert. Translate the user's natural language question
into a single valid SQLite query.

Database Schema:
Table: retail_sales
Columns:
  - transaction_id (INTEGER) PRIMARY KEY
  - date (TEXT)
  - customer_id (TEXT)
  - gender (TEXT)
  - age (INTEGER)
  - product_category (TEXT)
  - quantity (INTEGER)
  - price_per_unit (REAL)
  - total_amount (REAL)

Table: sales
Columns:
  - order_id (INTEGER) PRIMARY KEY
  - product (TEXT)
  - category (TEXT)
  - region (TEXT)
  - sales (REAL)
  - date (TEXT)

User Question:
Total revenue by product category

Strict Prompt Rules:
1. ONLY use the tables and columns mentioned in the schema above.
2. Return ONLY the raw SQL query.
3. Do NOT include explanations, markdown tags (like ```sql), or other text.
4. SQLite has no MONTH() or YEAR(). Use SUBSTR(date, 1, 7) for 'YYYY-MM' formatting.
```

### Explanation Prompt Structure

```text
You are a database analyst explaining query logic to business users.
Explain what this SQL query does in plain, concise English.
Describe what fields it retrieves, what calculations it performs, and any sorting.
Keep it strictly under two sentences. Do NOT use technical jargon like
'SELECT statement' or 'GROUP BY clause' — explain it conceptually.

SQL Query:
SELECT product_category, SUM(total_amount) AS revenue
FROM retail_sales
GROUP BY product_category
ORDER BY revenue DESC;
```

### Key Prompt Design Decisions

| Decision | Reason |
|---|---|
| Role assignment | Anchors model behavior as a database expert |
| Full schema injection | Prevents hallucinated table/column names |
| Raw SQL only instruction | Eliminates markdown wrappers and prose |
| SQLite-specific reminders | Prevents MySQL/PostgreSQL function usage |
| Two-sentence explanation limit | Keeps outputs concise for the UI card |
| Low temperature (0.1 for SQL, 0.2 for explanation) | Reduces randomness for deterministic output |

---

## 3. Fallback Rule-Based Engine

When Ollama is unavailable, `get_fallback_sql()` in `sql_generator.py` handles 14 query patterns:

**Retail Sales queries:**
- Total revenue by category
- Revenue by gender
- Top 5 customers by spending
- Monthly revenue trend
- Best selling category by quantity
- Average order value
- Any question mentioning: customer, transaction, product_category

**Legacy Sales queries:**
- Total sales by region
- Highest selling product
- Average sales
- Monthly sales trend
- Top 5 products by revenue
- Sales by category / product / region

Similarly, `get_fallback_explanation()` in `explanation_generator.py` pattern-matches against SQL structure (`AVG`, `GROUP BY`, `LIMIT`, `SUBSTR`) to generate template-based explanations for both datasets.

---

## 4. Challenges & Solutions

| Challenge | Solution |
|---|---|
| LLM wraps SQL in ```sql blocks | `clean_sql()` regex strips markdown wrappers |
| LLM uses MySQL functions (MONTH, YEAR) | Prompt explicitly instructs SUBSTR usage |
| LLM hallucinates column names | `confidence_score.py` penalizes unknown tokens |
| LLM returns prose instead of SQL | `clean_sql()` + validator rejects non-SELECT output |
| Ollama not installed / offline | Auto-detected via `/api/tags` ping, seamless fallback |
| Model not pulled (llama3.2 missing) | Sidebar badge warns user, fallback activates |

---

## 5. Confidence Scoring System

The confidence score (0–100%) provides transparency on query reliability:

| Dimension | Max Points | Method |
|---|---|---|
| Schema Alignment | 40 | Checks referenced tables/columns against `VALID_TABLES` and `VALID_COLUMNS` |
| Syntax Validity | 30 | Runs `EXPLAIN` on SQLite — passes only if query is executable |
| Intent Alignment | 30 | Matches NL keywords (average, total, highest) to SQL operations (AVG, SUM, DESC) |

A score of **0%** is automatically assigned to any query that fails the safety validator.

---

## 6. Limitations & Future Improvements

- **RAG for large schemas**: For databases with many tables, full schema injection bloats the prompt. A retrieval-augmented generation (RAG) approach would inject only the relevant tables based on the user's question.
- **Formal SQL parsing**: Replacing the token-based confidence scorer with a proper SQL AST parser (e.g., `sqlglot` or `sqlparse`) would enable more accurate structural validation.
- **Streaming responses**: The current Ollama call uses `stream: false`. Enabling streaming would allow the UI to show live token-by-token SQL generation.
- **Multi-turn conversation**: Future versions could maintain conversation context, allowing follow-up questions like "Now filter that by Female customers only."
- **Cloud LLM option**: Adding an optional Gemini or OpenAI API path alongside Ollama would provide a cloud-based fallback for environments where local models are impractical.
