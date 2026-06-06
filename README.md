# NL-To-SQL Analytics Agent

A production-ready AI analytics assistant that enables business users to query databases in plain English. The agent converts natural language questions into secure SQLite queries using a local LLM, validates query safety, executes them against a SQLite database, generates natural language explanations, calculates confidence scores, and visualizes analytical results using Plotly.

---

## Features

* Natural Language to SQL Conversion
* AI-Powered Query Generation using Ollama (Llama 3.2)
* Secure SQL Validation Layer
* SQLite Database Integration
* Interactive Plotly Visualizations
* Confidence Score Calculation
* Plain English Query Explanation
* Fallback Mode (No LLM Required)
* Automated Unit Testing

---

## Architecture Flow

```text
User Input (Plain English)
        ↓
Read Database Schema
        ↓
Generate SQL using AI
        ↓
Validate Query Safety
        ↓
Execute SQL Query
        ↓
Generate Results
    ├── Query Explanation
    ├── Confidence Score
    └── Plotly Charts
        ↓
Render Streamlit Dashboard
```

For more details, see:

```text
docs/architecture.md
```

---

## Tech Stack

| Component     | Technology         |
| ------------- | ------------------ |
| Frontend      | Streamlit          |
| Backend       | Python 3.10+       |
| Database      | SQLite             |
| AI Model      | Ollama (Llama 3.2) |
| Visualization | Plotly             |
| Testing       | Pytest             |

---

## Project Structure

```text
NL-TO-SQL-AGENT-main/
├── .gitignore
├── AI_Usage_Note.md          <-- (We just created this!)
├── app.py
├── create_db.py
├── query_history.json
├── README.md                 <-- (We just updated this!)
├── requirements.txt
├── retail_sales.css
├── agent/
│   ├── chart_generator.py
│   ├── explanation_generator.py
│   ├── insight_generator.py
│   ├── report_generator.py
│   ├── schema_tool.py
│   ├── sql_executor.py
│   ├── sql_generator.py
│   └── validator.py
├── database/
│   ├── dynamic_db.py
│   ├── schema_reader.py
│   ├── test_sales.db
│   └── uploaded_data.db
├── docs/
│   ├── ai_usage_note.md
│   └── architecture.md
├── sample_data/
│   ├── analytics_poc (1).db
│   ├── ecommerce.csv
│   └── retail_sales_dataset.csv
└── tests/
    └── test_agent.py         <-- (Our consolidated happy path test suite!)

```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd NL-To-SQL-Agent
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create Database

```bash
python create_db.py
```

This generates:

```text
database/uploaded_data.db
```

from:

```text
sample_data/sales.csv
```

---

## Running the Application

### Option A – Ollama Mode (Recommended)

Install Ollama:

```bash
ollama pull llama3.2
```

Run:

```bash
streamlit run app.py
```

### Option B – Fallback Mode

If Ollama is unavailable:

```bash
streamlit run app.py
```

The application automatically switches to its built-in rule-based engine.

---

## Sample Questions

* Total sales by region
* Highest selling product
* Average sales
* Monthly sales trend
* Top 5 products by revenue

---

## Running Tests

```bash
pytest
```

The test suite validates:

* Schema parsing
* SQL validation
* SQL execution
* Chart generation
* Confidence scoring

---

## Security Features

### Allowed

* SELECT queries
* WITH (CTE) queries

### Blocked

* DROP
* DELETE
* UPDATE
* INSERT
* ALTER
* TRUNCATE
* CREATE
* REPLACE

Additional Protection:

* Blocks stacked queries
* Prevents basic SQL injection attempts
* Assigns 0% confidence score to unsafe queries

---

## Assumptions & Limitations

* Ollama response time depends on local hardware.
* Complex schemas may occasionally produce incorrect SQL.
* Validator is rule-based and should be supplemented with read-only database permissions in production.
* The system supports analytics only and blocks all write operations.

---

## Team Members

| Name      | Role                                    |
| --------- | --------------------------------------- |
| Sridharan | Full Stack Development & AI Integration |
| Member 2  | Frontend Development                    |
| Member 3  | Testing & Documentation                 |

---

## License

This project is developed for academic and evaluation purposes.
