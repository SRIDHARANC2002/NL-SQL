# NL-To-SQL Analytics Agent

A production-ready AI analytics assistant that enables users to analyze datasets and SQLite databases using natural language. The application converts plain English questions into secure SQL queries, validates query safety, executes them against uploaded datasets, generates business insights, and visualizes analytical results using interactive Plotly charts.

---

# Business Problem

Business users often depend on technical teams to generate reports and perform database analysis. This dependency creates delays in decision-making and increases the workload on data teams.

Common challenges include:

* Lack of SQL knowledge among business users
* Delays in report generation
* Increased workload on analysts and developers
* Difficulty extracting insights quickly

This project addresses these challenges by allowing users to interact with databases using plain English.

---

# Proposed Solution

The NL-To-SQL Analytics Agent allows users to:

1. Upload a dataset or SQLite database
2. Automatically analyze the schema
3. Ask questions in natural language
4. Generate SQL queries using AI
5. Validate query safety
6. Execute queries securely
7. Generate business insights
8. Visualize results with charts
9. Download results and charts

---

# Architecture Overview

```text
User Uploads Dataset / Database
            ↓
Dataset Summary Generation
            ↓
Display Schema Information
(Major Columns, Rows, Data Types)
            ↓
User Enters Natural Language Question
            ↓
AI Generates SQL Query
(Ollama Llama 3.2 / Fallback Engine)
            ↓
SQL Validation
            ↓
Editable Manual SQL Query
            ↓
Query Execution
            ↓
Business Insight Generation
            ↓
Results Summary
(Rows, Columns, Numeric Columns)
            ↓
Results Table
            ↓
Interactive Chart Visualization
            ↓
CSV Export & Chart Image Download
```

---

# Key Features

## Dataset Upload

* Upload SQLite databases
* Automatic schema extraction
* Dataset overview generation
* Column identification
* Row and column statistics

## AI-Powered Analytics

* Natural Language to SQL conversion
* Schema-aware SQL generation
* SQL validation and security checks
* Editable SQL query support
* Business insight generation

## Query Results

* Query execution on uploaded data
* Results table display
* Result summary statistics
* Row count display
* Column count display
* Numeric column detection

## Interactive Visualizations

* Bar Charts
* Line Charts
* Pie Charts
* Scatter Charts
* Dynamic chart switching

## Export Features

* Download query results as CSV
* Download generated charts as PNG image

---

# Project Structure

```text
NL-TO-SQL-AGENT-main/
│
├── agent/
│   ├── chart_generator.py
│   ├── explanation_generator.py
│   ├── insight_generator.py
│   ├── report_generator.py
│   ├── schema_tool.py
│   ├── sql_executor.py
│   ├── sql_generator.py
│   └── validator.py
│
├── database/
│   ├── dynamic_db.py
│   ├── test_sales.db
│   └── uploaded_data.db
│
├── Demo/
│   └── Demo_Video_Link.md
│
├── docs/
│   └── ai_usage_note.md
│
├── Resume/
│   ├── Sridharan_Resume.pdf
│   └── Team_Member_Resume.pdf
│
├── sample_data/
│   ├── analytics_poc (1).db
│   ├── ecommerce.csv
│   └── retail_sales_dataset.csv
│
├── tests/
│   └── test_agent.py
│
├── .gitignore
├── AI_Usage_Note.md
├── app.py
├── create_db.py
├── README.md
├── requirements.txt
├── retail_sales.css
└── TEST_CASES.md
```

---

# Technology Stack

| Component     | Technology         |
| ------------- | ------------------ |
| Frontend      | Streamlit          |
| Backend       | Python 3.10+       |
| Database      | SQLite             |
| AI Model      | Ollama (Llama 3.2) |
| Visualization | Plotly             |
| Testing       | Pytest             |

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd NL-TO-SQL-AGENT-main
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Database Setup

Create and populate the SQLite database:

```bash
python create_db.py
```

This reads data from:

```text
sample_data/retail_sales_dataset.csv
```

and creates:

```text
database/uploaded_data.db
```

---

# Ollama Setup

Install Ollama from:

https://ollama.com

Pull the model:

```bash
ollama pull llama3.2
```

Verify installation:

```bash
ollama list
```

---

# Running the Application

## Option A – Ollama Mode

```bash
streamlit run app.py
```

The application will use the local Ollama model for SQL generation.

## Option B – Fallback Mode

If Ollama is unavailable:

```bash
streamlit run app.py
```

The application automatically switches to the built-in rule-based SQL generation engine.

---

# User Workflow

## Step 1: Upload Dataset

Upload a SQLite database or supported dataset.

## Step 2: Dataset Summary

The system automatically displays:

* Number of rows
* Number of columns
* Column names
* Dataset schema overview

## Step 3: Ask a Question

Example:

```text
Show total revenue by product category
```

## Step 4: SQL Generation

The AI model generates a SQL query based on the uploaded schema.

## Step 5: Edit SQL (Optional)

Users can modify the generated SQL query manually before execution.

## Step 6: Execute Query

The query is validated and executed safely.

## Step 7: View Results

The dashboard displays:

* Business insights
* Query summary
* Result table
* Number of rows returned
* Number of columns returned
* Numeric column information

## Step 8: Visualize Results

Choose chart types dynamically:

* Bar Chart
* Line Chart
* Pie Chart
* Scatter Chart

## Step 9: Download Outputs

Users can:

* Download results as CSV
* Download chart as PNG image

---

# Sample Questions

* Total revenue by product category
* Monthly sales trend
* Top selling product
* Revenue by region
* Revenue vs Quantity
* Average sales by category
* Top 5 products by revenue

---

# Security Features

The SQL validator protects the database by blocking unsafe queries.

### Allowed

* SELECT queries
* WITH (CTE) queries

### Blocked

* DROP
* DELETE
* UPDATE
* INSERT
* ALTER
* CREATE
* TRUNCATE
* REPLACE

### Additional Protection

* Multi-statement queries blocked
* SQL injection prevention
* Read-only analytics environment

---

# Testing

Run automated tests:

```bash
pytest tests/test_agent.py
```

Covered Components:

* Schema Extraction
* SQL Validation
* SQL Generation
* Query Execution
* Chart Generation

For detailed testing documentation:

```text
TEST_CASES.md
```

---

# AI Usage Documentation

Detailed AI usage notes are available in:

```text
AI_Usage_Note.md
```

---

# Assumptions & Limitations

### Local AI Performance

Response time depends on local hardware and Ollama availability.

### Schema Complexity

Very complex schemas may occasionally result in inaccurate SQL generation.

### Security Scope

The validator uses rule-based filtering and should be combined with read-only database permissions in production environments.

### Analytics Only

The system is designed for analytics and reporting. Database write operations are intentionally blocked.

---

# Deliverables

* Source Code
* README Documentation
* AI Usage Note
* Sample Datasets
* Test Cases
* Demo Video
* Team Member Resumes

---
# Demo Video

Watch the project demonstration here:

[Demo Video](https://your-demo-video-link)
[TEST_CASES.txt](https://drive.google.com/file/d/1hPyKMJ9VnmND1YhonZ5B9zJPWitG9zCH/view?usp=sharing)
[SampleData] (https://drive.google.com/file/d/1G6eOmasd9YvDk9NlTGZQVVxxtEEa_5K7/view?usp=sharing)

---

# Team Resumes

- [Sridharan Resume](https://drive.google.com/file/d/1FsqizgchbN_-73A9V6yPBhQreOPBwpUN/view?usp=sharing)
- [Team Member 2 Resume](https://your-resume-link)
- [Team Member 3 Resume](https://your-resume-link)







# License

This project was developed for academic, learning, and evaluation purposes.
