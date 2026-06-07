# AI Usage Note

## Project Name

NL-To-SQL Analytics Agent

## AI Tools Used

* ChatGPT
* Ollama (Llama 3.2)

---

## 1. What AI Helped With During Development

AI was used as a development assistant throughout the project lifecycle. The following areas were supported by AI:

### Project Architecture

* Assisted in designing the modular architecture of the application.
* Suggested separation of functionalities into modules such as:

  * schema_tool.py
  * sql_generator.py
  * validator.py
  * sql_executor.py
  * chart_generator.py
  * explanation_generator.py
  * insight_generator.py

### Streamlit Dashboard Development

* Assisted in building the Streamlit user interface.
* Suggested layouts for query input, result display, and visualization sections.
* Helped improve responsiveness and overall user experience.

### SQL Generation Workflow

* Assisted in designing the Natural Language to SQL workflow.
* Helped create prompts for generating SQL queries using Ollama.
* Suggested fallback mechanisms when the local AI model is unavailable.

### SQL Validation and Security

* Assisted in implementing validation rules to ensure safe query execution.
* Suggested techniques for blocking unsafe SQL commands such as:

  * DROP
  * DELETE
  * UPDATE
  * INSERT
  * ALTER
  * TRUNCATE
  * CREATE
  * REPLACE

### Data Visualization

* Assisted in generating Plotly charts.
* Suggested chart selection logic for:

  * Bar Charts
  * Line Charts
  * Pie Charts
  * Scatter Charts

### Testing and Debugging

* Helped identify and fix coding issues.
* Assisted in creating test cases for:

  * Schema extraction
  * SQL validation
  * SQL execution
  * Chart generation

---

## 2. Challenges Encountered with AI

### Schema Hallucination

At times, AI generated SQL queries using non-existent table names or columns when schema information was not provided explicitly.

### Context Issues

When project files were renamed or modified, AI occasionally referenced outdated modules or functions.

### SQL Accuracy

Some generated SQL queries required manual verification and correction to match the database schema accurately.

### UI Adjustments

Several iterations were required to achieve the final Streamlit layout and visualization appearance.

---

## 3. Best Prompts Used

### Prompt 1

Generate a SQLite query for the user's question using only the provided database schema. Return only executable SQL.

### Prompt 2

Review the generated SQL query and determine whether it contains unsafe operations such as DROP, DELETE, UPDATE, INSERT, ALTER, CREATE, REPLACE, or multiple statements.

### Prompt 3

Create a responsive Streamlit dashboard that accepts natural language questions, displays generated SQL, query results, and Plotly visualizations.

### Prompt 4

Generate suitable Plotly visualizations automatically based on the structure of the query result dataset.

### Prompt 5

Review the entire repository and identify any missing deliverables, documentation, datasets, tests, or project requirements.

---

## 4. Human Contribution

Although AI assisted with code generation, debugging, testing, and documentation, all implementation decisions, integration work, testing, validation, and final review were performed manually.

The developer reviewed all AI-generated outputs, verified SQL execution, validated results, and ensured that the final application met the project requirements.

---

## Conclusion

AI was used as a development assistant to accelerate coding, debugging, testing, visualization, and documentation tasks. Final implementation, verification, and project integration were completed manually by the development team.
