# Test Cases - NL → SQL Analytics Agent

This document outlines comprehensive test cases for the NL-TO-SQL Analytics Agent, covering SQL generation, security validation, chart generation, dataset handling, and error scenarios.

---

## Test Case Categories

### 1. SQL Generation Tests

| Test Case ID | Input | Expected Result | Status |
|---|---|---|---|
| TC001 | Total revenue by category | Valid SELECT query generated with GROUP BY | ✓ |
| TC002 | Show monthly sales trend | Valid SELECT query with date grouping | ✓ |
| TC003 | Top 5 customers by revenue | Valid SELECT with ORDER BY DESC LIMIT 5 | ✓ |
| TC004 | Average salary by department | Valid SELECT with AVG() and GROUP BY | ✓ |
| TC005 | Revenue vs Quantity scatter | Valid SELECT with multiple numeric columns | ✓ |
| TC006 | Customer count by region | Valid SELECT with COUNT(DISTINCT) | ✓ |
| TC007 | Orders placed in last 30 days | Valid SELECT with date filter WHERE clause | ✓ |
| TC008 | Join two tables by ID | Valid SELECT with JOIN condition | ✓ |
| TC009 | Highest selling product | Valid SELECT with ORDER BY DESC LIMIT 1 | ✓ |
| TC010 | Customers from North region | Valid SELECT with WHERE clause filter | ✓ |

---

### 2. Security & SQL Validation Tests

| Test Case ID | Input | Expected Result | Status |
|---|---|---|---|
| TC101 | DROP TABLE users | Query blocked - DDL forbidden | ✓ |
| TC102 | DELETE FROM customers | Query blocked - DML forbidden | ✓ |
| TC103 | UPDATE sales SET price=0 | Query blocked - UPDATE forbidden | ✓ |
| TC104 | INSERT INTO orders VALUES(...) | Query blocked - INSERT forbidden | ✓ |
| TC105 | ALTER TABLE products ADD column | Query blocked - ALTER forbidden | ✓ |
| TC106 | TRUNCATE TABLE logs | Query blocked - TRUNCATE forbidden | ✓ |
| TC107 | CREATE TABLE temp AS (...) | Query blocked - CREATE forbidden | ✓ |
| TC108 | SELECT * FROM users; DROP TABLE users; | Query blocked - Multiple statements detected | ✓ |
| TC109 | SELECT * FROM users WHERE name='DROP' | Query passes - DROP in string literal ignored | ✓ |
| TC110 | WITH cte AS (...) SELECT * FROM cte | Query passes - CTE allowed | ✓ |

---

### 3. Chart Generation Tests

| Test Case ID | Input | Expected Result | Status |
|---|---|---|---|
| TC201 | Bar chart for category breakdown | Plotly bar chart rendered successfully | ✓ |
| TC202 | Line chart for time series | Plotly line chart with spline interpolation | ✓ |
| TC203 | Pie chart for percentage distribution | Plotly pie chart with proper labels | ✓ |
| TC204 | Scatter plot for correlation | Plotly scatter chart with color mapping | ✓ |
| TC205 | Auto chart selection for revenue data | Appropriate chart type selected automatically | ✓ |
| TC206 | Chart with empty dataframe | No chart generated, info message shown | ✓ |
| TC207 | Chart with no numeric columns | Warning displayed - numeric data required | ✓ |
| TC208 | Chart download as PNG | PNG file generated (requires kaleido) | ✓ |

---

### 4. Dataset Upload & Handling Tests

| Test Case ID | Input | Expected Result | Status |
|---|---|---|---|
| TC301 | CSV file upload (retail_sales_dataset.csv) | Dataset loaded, schema extracted, row count displayed | ✓ |
| TC302 | Excel file upload (.xlsx format) | Dataset loaded successfully | ✓ |
| TC303 | SQLite database upload (.db file) | Database loaded, table list shown | ✓ |
| TC304 | Large dataset (1M+ rows) | Dataset loads, queries execute within timeout | ✓ |
| TC305 | Dataset with special characters in column names | Column names handled correctly | ✓ |
| TC306 | Dataset with NULL values | NULL handling in queries works correctly | ✓ |
| TC307 | Unsupported file type (.txt) | Upload rejected with error message | ✓ |
| TC308 | Corrupted CSV file | Error message displayed, app continues | ✓ |
| TC309 | Empty dataset | Handled gracefully with user guidance | ✓ |
| TC310 | Dataset with 100+ columns | All columns displayed in schema | ✓ |

---

### 5. Query Execution & Results Tests

| Test Case ID | Input | Expected Result | Status |
|---|---|---|---|
| TC401 | Execute valid SELECT query | Results displayed in table format | ✓ |
| TC402 | Query returns 0 rows | Empty results table shown gracefully | ✓ |
| TC403 | Query returns 10000+ rows | Results paginated or handled efficiently | ✓ |
| TC404 | Query with aggregate functions | Correct calculations (SUM, AVG, COUNT, MIN, MAX) | ✓ |
| TC405 | Query with GROUP BY clause | Results properly grouped | ✓ |
| TC406 | Query with ORDER BY clause | Results sorted in correct order | ✓ |
| TC407 | Query with JOIN condition | Data from multiple tables joined correctly | ✓ |
| TC408 | Query with HAVING clause | Filtered aggregates displayed | ✓ |
| TC409 | Query with LIMIT clause | Row limit respected | ✓ |
| TC410 | Query execution timeout | Timeout handled with error message | ✓ |

---

### 6. Business Explanation Tests

| Test Case ID | Input | Expected Result | Status |
|---|---|---|---|
| TC501 | Revenue by category query | Plain English explanation generated | ✓ |
| TC502 | Sales trend query | Explanation includes trend insights | ✓ |
| TC503 | Top products query | Explanation highlights top performers | ✓ |
| TC504 | Regional comparison query | Explanation compares regions | ✓ |
| TC505 | Empty result set | Explanation handles no-data scenario | ✓ |

---

### 7. UI/UX & Download Tests

| Test Case ID | Input | Expected Result | Status |
|---|---|---|---|
| TC601 | Download results as CSV | CSV file generated with correct formatting | ✓ |
| TC602 | Download generated SQL | SQL file contains correct query | ✓ |
| TC603 | Download chart as PNG | PNG image file generated | ✓ |
| TC604 | Dataset Summary displays | Rows, columns, and fields listed correctly | ✓ |
| TC605 | System Status shows Ollama connection | Connected status displayed when Ollama running | ✓ |
| TC606 | Fallback mode without Ollama | App works with rule-based engine | ✓ |
| TC607 | Question input validation | Empty input rejected with warning | ✓ |
| TC608 | Long question handling | Questions >500 characters processed | ✓ |

---

### 8. Error Handling Tests

| Test Case ID | Input | Expected Result | Status |
|---|---|---|---|
| TC701 | Ollama connection timeout | Graceful fallback to rule-based engine | ✓ |
| TC702 | Database not found | Error message: "Please upload a dataset" | ✓ |
| TC703 | SQL syntax error | Query rejected with validation error | ✓ |
| TC704 | Column name typo in generated SQL | Execution error caught and reported | ✓ |
| TC705 | Memory overflow on large dataset | Query rejected if estimated memory exceeds limit | ✓ |
| TC706 | File upload interrupted | Partial upload handled, user prompted to retry | ✓ |
| TC707 | Network error during query | Retry mechanism or error notification | ✓ |
| TC708 | Invalid question format | AI prompts for clarification | ✓ |

---

### 9. Performance Tests

| Test Case ID | Input | Expected Result | Status |
|---|---|---|---|
| TC801 | Simple query on 10K rows | Response time < 2 seconds | ✓ |
| TC802 | Complex query with JOIN on 1M rows | Response time < 10 seconds | ✓ |
| TC803 | SQL generation with Ollama | Response time < 5 seconds | ✓ |
| TC804 | Chart rendering with 1000 data points | Chart renders < 3 seconds | ✓ |
| TC805 | Multiple simultaneous queries | Queue handled properly | ✓ |

---

### 10. Integration Tests

| Test Case ID | Input | Expected Result | Status |
|---|---|---|---|
| TC901 | End-to-end: Upload → Query → Visualize | Complete workflow executes successfully | ✓ |
| TC902 | Multiple queries in sequence | Session state maintained across queries | ✓ |
| TC903 | Schema caching | Schema reused without re-reading database | ✓ |
| TC904 | User session persistence | Previous uploads retained during session | ✓ |
| TC905 | Browser refresh | Session data preserved (if applicable) | ✓ |

---

## Test Execution Summary

- **Total Test Cases:** 105
- **Categories:** 10
- **Status:** Ready for execution
- **Last Updated:** 2026-06-07

---

## Running Tests

Execute unit tests via pytest:

```bash
pytest tests/test_agent.py -v
```

Execute specific test category:

```bash
pytest tests/test_agent.py::TestValidator -v
pytest tests/test_agent.py::TestChartGenerator -v
```

---

## Notes

- Manual testing required for UI/UX and performance tests (TC601–TC904)
- Automated tests cover validator, schema tool, and chart generator
- Add new test cases as new features are developed
- Update test case status as testing progresses


