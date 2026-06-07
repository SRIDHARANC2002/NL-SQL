import streamlit as st
import pandas as pd
import os

from database.dynamic_db import (
    create_database_from_dataframe,
    get_schema,
    get_row_count,
    get_column_names
)
<<<<<<< HEAD
=======

>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7
from agent.sql_generator import (
    generate_sql,
    check_ollama_status
)
<<<<<<< HEAD
from agent.agent_loop import agent_loop_generate_and_run
=======

>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7
from agent.validator import validate_sql
from agent.sql_executor import execute_sql
from agent.chart_generator import create_chart
from agent.explanation_generator import explain_sql
<<<<<<< HEAD
=======
# from agent.insight_generator import generate_insights

>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
<<<<<<< HEAD
=======

>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7
st.set_page_config(
    page_title="NL → SQL Analytics Agent",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------
<<<<<<< HEAD
st.markdown("""
<style>

/* ---------- FONT & BASE ---------- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

:root {
    --brand: #4f46e5;
    --brand-dark: #4338ca;
    --brand-light: #6366f1;
    --ink: #0f172a;
    --muted: #64748b;
    --line: #e2e8f0;
    --surface: #ffffff;
    --surface-alt: #f8fafc;
}

.main .block-container {
    padding-top: 2.2rem;
    max-width: 1250px;
}

/* ---------- HEADINGS ---------- */
.main-title {
    text-align: center;
    font-size: 44px;
    font-weight: 800;
    letter-spacing: -1px;
    background: linear-gradient(135deg, var(--brand) 0%, var(--brand-light) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 6px;
}

.sub-title {
    text-align: center;
    color: var(--muted);
    font-size: 16px;
    margin-bottom: 28px;
}

h2, h3 {
    color: var(--ink) !important;
    font-weight: 700 !important;
    letter-spacing: -0.3px;
}

/* ---------- BUTTONS ---------- */
div.stButton > button {
    background: linear-gradient(135deg, var(--brand) 0%, var(--brand-light) 100%);
    color: #ffffff;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 0.55rem 1.2rem;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.28);
    transition: all 0.18s ease;
}

div.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(79, 70, 229, 0.40);
    background: linear-gradient(135deg, var(--brand-dark) 0%, var(--brand) 100%);
}

div.stButton > button:active {
    transform: translateY(0);
}

/* ---------- INPUTS ---------- */
.stTextInput > div > div > input,
.stTextArea textarea,
.stSelectbox > div > div {
    border-radius: 10px !important;
    border: 1px solid var(--line) !important;
}

.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: var(--brand) !important;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.12) !important;
}

/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"] {
    background: var(--surface-alt);
    border-right: 1px solid var(--line);
}

section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] .stSubheader {
    color: var(--ink);
}

/* ---------- DATASET SUMMARY CARD ---------- */
.dataset-summary-card {
    background: var(--surface);
    color: var(--ink);
    padding: 22px 24px;
    border: 1px solid var(--line);
    border-radius: 16px;
    margin-top: 12px;
    box-shadow: 0 4px 24px rgba(15, 23, 42, 0.05);
=======

st.markdown("""
<style>

.main-title {
    text-align:center;
    font-size:42px;
    font-weight:bold;
    margin-bottom:10px;
}

.sub-title {
    text-align:center;
    color:#666;
    margin-bottom:25px;
}

.metric-box {
    padding:15px;
    border-radius:10px;
    background:#f8f9fa;
    border:1px solid #ddd;
}

/* Style the primary button placed in the left column */
div.stButton > button:first-child {
    background-color: #2b6cb0;
    color: #ffffff;
    height: 38px;
    width: 140px;
    border-radius: 8px;
    border: 1px solid #1e4367;
    font-weight: 600;
}

div.stButton > button:first-child:hover {
    background-color: #1f5a96;
}

.summary-table {
    width: 400px;
    margin: 15px 0;
    border-collapse: collapse;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.summary-table th {
    background: #1e293b;
    color: white;
    text-align: left;
    padding: 12px;
}

.summary-table td {
    padding: 10px 12px;
    border-bottom: 1px solid #e5e7eb;
}

.summary-table td:last-child {
    text-align: center;
    font-weight: 600;
}

table {
    width: auto !important;
    margin: 0 auto;
    border-collapse: collapse;
    table-layout: auto;
}

table th,
table td {
    padding: 8px 12px;
    text-align: left;
    vertical-align: middle;
}

table th {
    background: #f8fafc;
    font-weight: 600;
}

table td:last-child {
    text-align: right;
}

.dataset-summary-card {
    background: #ffffff;
    color: #000000;
    padding: 18px 20px;
    border: 1px solid #d1d5db;
    border-radius: 12px;
    margin-top: 12px;
>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7
}

.dataset-summary-row {
    display: flex;
    flex-wrap: wrap;
<<<<<<< HEAD
    gap: 12px;
    align-items: center;
    margin-bottom: 12px;
}

.dataset-summary-label {
    font-size: 13px;
    font-weight: 600;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.4px;
}

.dataset-summary-value {
    font-size: 18px;
    font-weight: 800;
    color: var(--brand);
}

.dataset-summary-fields { display: block; }

.dataset-summary-list {
    list-style: none;
    margin: 10px 0 0 0;
    padding: 0;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.dataset-summary-list li {
    margin: 0;
}

.dataset-summary-field {
    display: inline-block;
    background: rgba(79, 70, 229, 0.08);
    color: var(--brand-dark);
    font-weight: 600;
    font-size: 13px;
    padding: 5px 12px;
    border-radius: 9999px;
    border: 1px solid rgba(79, 70, 229, 0.18);
}

/* ---------- SUMMARY / RESULT TABLES ---------- */
.summary-table {
    width: 100%;
    margin: 12px 0;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 14px rgba(15, 23, 42, 0.06);
    border: 1px solid var(--line);
}

.summary-table th {
    background: var(--ink);
    color: #ffffff;
    text-align: left;
    padding: 12px 14px;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}

.summary-table td {
    padding: 11px 14px;
    border-bottom: 1px solid var(--line);
    color: var(--ink);
    font-size: 14px;
}

.summary-table tbody tr:last-child td { border-bottom: none; }
.summary-table tbody tr:nth-child(even) { background: var(--surface-alt); }
.summary-table tbody tr:hover { background: rgba(79, 70, 229, 0.05); }

/* ---------- CODE BLOCKS ---------- */
.stCodeBlock, pre {
    border-radius: 12px !important;
    border: 1px solid var(--line);
}

/* ---------- ALERTS ---------- */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: none !important;
}

/* ---------- EXPANDER ---------- */
.streamlit-expanderHeader, [data-testid="stExpander"] details summary {
    border-radius: 10px !important;
    font-weight: 600;
}

/* ---------- SCROLLBAR ---------- */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: var(--surface-alt); }
::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 9999px;
    border: 2px solid var(--surface-alt);
}
::-webkit-scrollbar-thumb:hover { background: var(--brand-light); }

=======
    gap: 14px;
    align-items: center;
    margin-bottom: 8px;
}

.dataset-summary-label {
    font-size: 14px;
    font-weight: 600;
    color: #000000;
}

.dataset-summary-value {
    font-size: 16px;
    font-weight: 700;
    color: #000000;
}

.dataset-summary-fields {
    display: block;
}

.dataset-summary-list {
    margin: 6px 0 0 18px;
    padding: 0;
    list-style-position: inside;
}

.dataset-summary-list li {
    margin-bottom: 6px;
}

.dataset-summary-field {
    color: #047857;
    font-weight: 700;
}

>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
<<<<<<< HEAD
if "dataset_loaded" not in st.session_state:
    st.session_state.dataset_loaded = False
if "schema" not in st.session_state:
    st.session_state.schema = ""
=======

if "dataset_loaded" not in st.session_state:
    st.session_state.dataset_loaded = False

if "schema" not in st.session_state:
    st.session_state.schema = ""

>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7
if "question" not in st.session_state:
    st.session_state.question = ""

# --------------------------------------------------
# HEADER
# --------------------------------------------------
<<<<<<< HEAD
st.markdown(
    '<div class="main-title">NL → SQL Analytics Agent</div>',
    unsafe_allow_html=True
)
=======

st.markdown(
    '<div class="main-title"> NL → SQL Analytics Agent</div>',
    unsafe_allow_html=True
)

>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7
st.markdown(
    '<div class="sub-title">Upload CSV, Excel, or a SQLite database file and ask questions in plain English</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
<<<<<<< HEAD
st.sidebar.markdown("### 👋 Welcome\n\nUpload your dataset and ask questions in plain English.")

st.sidebar.subheader("🤖 LLM Provider")
provider_choice = st.sidebar.radio(
    "Select Provider",
    ["Local (Ollama)", "External (Groq API)"],
    index=0
)

api_key = None

if provider_choice == "External (Groq API)":
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.environ.get("GROQ_API_KEY")
    if api_key:
        st.sidebar.success("Groq Connected")
    else:
        st.sidebar.error("⚠️ Groq API Key Missing! Please add GROQ_API_KEY to your .env file.")
else:
    st.sidebar.subheader("⚙️ System Status")
    ollama_running, has_model, models = check_ollama_status()
    if ollama_running and has_model:
        st.sidebar.success("Ollama Connected")
    else:
        st.sidebar.error("Ollama Not Available")
=======

# Sidebar welcome and system status
st.sidebar.markdown("### 👋 Welcome\n\nUpload your dataset and ask questions in plain English.")

st.sidebar.subheader("⚙️ System Status")

ollama_running, has_model, models = check_ollama_status()

if ollama_running and has_model:
    st.sidebar.success(" Ollama Connected")
else:
    st.sidebar.error("Ollama Not Available")
>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7

# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------
<<<<<<< HEAD
=======

>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7
st.sidebar.subheader("📂 Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Choose CSV, Excel, or SQLite DB File",
    type=["csv", "xlsx", "xls", "db", "sqlite", "sqlite3"]
)

if uploaded_file:
<<<<<<< HEAD
    try:
=======

    try:

>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7
        filename = uploaded_file.name.lower()

        if filename.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            create_database_from_dataframe(df)

        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
            create_database_from_dataframe(df)

        elif filename.endswith((".db", ".sqlite", ".sqlite3")):
            os.makedirs("database", exist_ok=True)
<<<<<<< HEAD
            with open("database/uploaded_data.db", "wb") as db_file:
                db_file.write(uploaded_file.getbuffer())
=======

            with open("database/uploaded_data.db", "wb") as db_file:
                db_file.write(uploaded_file.getbuffer())

>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7
            st.sidebar.success("SQLite database uploaded")
            st.session_state.dataset_loaded = True

        else:
            raise ValueError("Unsupported file type. Please upload CSV, Excel, or SQLite database files.")

<<<<<<< HEAD
        if filename.endswith((".csv", ".xlsx", ".xls")):
            st.session_state.dataset_loaded = True

        if st.session_state.dataset_loaded:
            st.session_state.schema = get_schema()

    except Exception as e:
        st.error(f"Dataset Upload Failed: {str(e)}")
=======
        if "dataset_loaded" in st.session_state and st.session_state.dataset_loaded:
            schema = get_schema()
            st.session_state.schema = schema

        # Dataset preview removed per user request

    except Exception as e:

        st.error(
            f"Dataset Upload Failed: {str(e)}"
        )

>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7
        st.stop()

# --------------------------------------------------
# STOP IF NO DATASET
# --------------------------------------------------
<<<<<<< HEAD
if not st.session_state.dataset_loaded:
    st.info("Please upload a CSV or Excel dataset to begin.")
    st.stop()

# --------------------------------------------------
# DATASET SUMMARY
# --------------------------------------------------
st.subheader("Dataset Summary")
=======

if not st.session_state.dataset_loaded:

    st.info(
        "Please upload a CSV or Excel dataset to begin."
    )

    st.stop()
# --------------------------------------------------
# QUESTION INPUT
# --------------------------------------------------

st.subheader("Dataset Summary")

>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7
st.markdown(
    "This dataset has been uploaded successfully. Use the fields below when asking questions in plain English."
)

columns = get_column_names()
row_count = get_row_count()
column_count = len(columns)

summary_html = f"""
<div class="dataset-summary-card">
    <div class="dataset-summary-row">
        <span class="dataset-summary-label">Rows:</span>
        <span class="dataset-summary-value">{row_count}</span>
        <span class="dataset-summary-label">Columns:</span>
        <span class="dataset-summary-value">{column_count}</span>
<<<<<<< HEAD
=======
    </div>
    <div class="dataset-summary-row">
>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7
        <span class="dataset-summary-label">Table:</span>
        <span class="dataset-summary-value">uploaded_data</span>
    </div>
    <div class="dataset-summary-row dataset-summary-fields">
        <span class="dataset-summary-label">Fields:</span>
        <ul class="dataset-summary-list">
            {''.join([f'<li><span class="dataset-summary-field">{col}</span></li>' for col in columns])}
        </ul>
    </div>
</div>
"""
<<<<<<< HEAD
st.markdown(summary_html, unsafe_allow_html=True)

# --------------------------------------------------
# QUESTION INPUT
# --------------------------------------------------
=======

st.markdown(summary_html, unsafe_allow_html=True)

>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7
st.subheader("Ask Your Question")

question = st.text_input(
    "Enter your question",
    value="",
    placeholder="Example: Average salary by department"
)

<<<<<<< HEAD
generate_button = st.button("Generate SQL & Analyze", use_container_width=True)
=======
generate_button = st.button(
    "Generate SQL & Analyze",
    use_container_width=True
)
>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7

# --------------------------------------------------
# RUN ANALYSIS
# --------------------------------------------------
<<<<<<< HEAD
if generate_button:
    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    schema = st.session_state.schema
    provider_val = "groq" if provider_choice == "External (Groq API)" else "ollama"

    if provider_val == "groq" and not api_key:
        st.error("Please provide a Groq API Key in the sidebar.")
        st.stop()

    if provider_val == "ollama":
        running, has_mod, _ = check_ollama_status()
        if not running or not has_mod:
            st.error("Ollama is not running or the required model is missing.")
            st.stop()

    with st.spinner(f"Agent Loop: Generating and verifying SQL via {provider_choice}..."):
        try:
            sql_to_run, results_df = agent_loop_generate_and_run(
                question=question,
                schema=schema,
                execute_func=execute_sql,
                validate_func=validate_sql,
                provider=provider_val,
                api_key=api_key,
                max_retries=3
            )
            st.session_state.executed_sql = sql_to_run
            st.session_state.results_df = results_df
            st.session_state.question = question
        except Exception as e:
            st.error(f"Agent Loop Failed: {str(e)}")
            st.stop()

    st.subheader("Executed SQL Query")
    st.code(st.session_state.executed_sql, language="sql", line_numbers=True)

# --------------------------------------------------
# EXECUTE QUERY / MANUAL EDITOR
# --------------------------------------------------
if "executed_sql" in st.session_state:
    with st.expander("🛠️ Manual SQL Editor"):
        manual_sql = st.text_area(
            "Edit or enter SQL manually:",
            value=st.session_state.get('executed_sql', ''),
            height=200,
        )
        if st.button("Run Manual SQL"):
            try:
                manual_results_df = execute_sql(manual_sql)
                st.success("Manual SQL executed successfully.")
                st.session_state.results_df = manual_results_df
                st.session_state.executed_sql = manual_sql
            except Exception as e:
                st.error(f"Manual execution failed: {str(e)}")

    sql_query = st.session_state.executed_sql
    results_df = st.session_state.results_df

    st.markdown(
        "<h3>Query Execution &nbsp; <span style='color:#16a34a; font-weight:700;'>✅ Success</span></h3>",
        unsafe_allow_html=True
    )

    # ---------- EXPLANATION ----------
    st.subheader("Business Explanation")
    try:
        provider_val = "groq" if provider_choice == "External (Groq API)" else "ollama"
        explanation = explain_sql(sql_query, provider=provider_val, api_key=api_key)
        st.markdown(explanation)
    except Exception:
        st.markdown("Explanation could not be generated.")
        explanation = ""

    # ---------- RESULT METRICS + RESULTS ----------
=======

if generate_button:

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

        st.stop()

    schema = st.session_state.schema

    # ------------------------------------------
    # GENERATE SQL (preview)
    # ------------------------------------------

    with st.spinner(
        "Generating SQL using Ollama..."
    ):

        try:

            generated_sql = generate_sql(
                question,
                schema
            )

            st.session_state.generated_sql_preview = generated_sql
            st.session_state.manual_sql = generated_sql
            st.session_state.question = question
            st.session_state.executed_sql = generated_sql

        except Exception as e:

            st.error(
                f"SQL Generation Failed: {str(e)}"
            )

            st.stop()

# ------------------------------------------
# DISPLAY GENERATED SQL + MANUAL ENTRY
# ------------------------------------------

if "generated_sql_preview" in st.session_state:

    generated_sql = st.session_state.generated_sql_preview

    if "manual_sql" not in st.session_state:
        st.session_state.manual_sql = generated_sql

    left, right = st.columns([1, 1])

    with left:
        st.subheader("Generated SQL")
        st.code(
            generated_sql,
            language="sql",
            line_numbers=True
        )

    with right:
        st.subheader("Manual SQL")
        st.text_area(
            "",
            key="manual_sql",
            height=220
        )

        run_sql_button = st.button("Run SQL", use_container_width=True)

    if run_sql_button:

        sql_to_run = st.session_state.manual_sql.strip()

        if not sql_to_run:

            st.warning(
                "Please enter SQL to run."
            )

        else:

            is_valid = validate_sql(sql_to_run)

            if not is_valid:

                st.error(
                    """
                    SQL Validation Failed

                    The query contains restricted operations or invalid syntax.
                    """
                )

            else:

                st.session_state.executed_sql = sql_to_run
                if "results_df" in st.session_state:
                    del st.session_state["results_df"]

# --------------------------------------------------
# EXECUTE QUERY
# --------------------------------------------------

if "executed_sql" in st.session_state:

    execution_status = "pending"
    sql_query = st.session_state.executed_sql

    try:

        with st.spinner(
            "Executing query..."
        ):

            results_df = execute_sql(
                sql_query
            )

        st.session_state.results_df = results_df
        execution_status = "success"

    except Exception as e:

        st.error(
            f"❌ Query Execution Failed: {str(e)}"
        )

        st.stop()

    # Display heading with status on the same line
    if execution_status == "success":
        st.markdown("<h3>Query Execution   <span style='color: green; font-weight: bold;'>✅ Success</span></h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h3>Query Execution</h3>", unsafe_allow_html=True)

    # --------------------------------------------------
    # EXPLANATION
    # --------------------------------------------------

    st.subheader("Business Explanation")

    try:

        explanation = explain_sql(
            sql_query
        )

        st.markdown(explanation)

    except Exception:

        st.markdown(
            "Explanation could not be generated."
        )

        explanation = ""

    # Confidence score display removed per user request

    # --------------------------------------------------
    # RESULT METRICS + QUERY RESULTS (side by side)
    # --------------------------------------------------

>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7
    left_col, right_col = st.columns([1, 1], gap="small")

    with left_col:
        st.subheader("Result Summary")
<<<<<<< HEAD
        numeric_count = len(results_df.select_dtypes(include="number").columns)
        summary_html = f"""
        <table class='summary-table'>
            <thead>
                <tr><th>Metric</th><th>Value</th></tr>
=======

        numeric_count = len(
            results_df.select_dtypes(include="number").columns
        )

        summary_html = f"""
        <table class='summary-table'>
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7
            </thead>
            <tbody>
                <tr><td>Rows Returned</td><td>{len(results_df)}</td></tr>
                <tr><td>Columns Returned</td><td>{len(results_df.columns)}</td></tr>
                <tr><td>Numeric Fields</td><td>{numeric_count}</td></tr>
            </tbody>
        </table>
        """
<<<<<<< HEAD
=======

>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7
        st.markdown(summary_html, unsafe_allow_html=True)

    with right_col:
        st.subheader("Query Results")
<<<<<<< HEAD
        if results_df.empty:
            st.warning("No records returned.")
        else:
=======

        if results_df.empty:

            st.warning(
                "No records returned."
            )

        else:

            # Convert dataframe to HTML table with same styling as summary
>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7
            html_table = results_df.to_html(
                classes='summary-table',
                border=0,
                index=False,
                justify='left'
            )
<<<<<<< HEAD
            st.markdown(html_table, unsafe_allow_html=True)

# --------------------------------------------------
# CHARTS
# --------------------------------------------------
if "results_df" in st.session_state:
    results_df = st.session_state.results_df

    if not results_df.empty:
        col1, col2, col3 = st.columns([2.5, 1.5, 6], gap="small", vertical_alignment="center")
        with col1:
            st.subheader("Visualization")
=======
            
            st.markdown(html_table, unsafe_allow_html=True)
        # --------------------------------------------------
# CHARTS
# --------------------------------------------------

if "results_df" in st.session_state:

    results_df = st.session_state.results_df

    if not results_df.empty:

        # Visualization header and Chart type selector
        col1, col2, col3 = st.columns([2.5, 1.5, 6], gap="small", vertical_alignment="center")
        with col1:
            st.subheader(" Visualization")
>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7
        with col2:
            chart_type = st.selectbox(
                "Chart Type",
                ["Bar", "Line", "Pie", "Scatter", "Auto"],
                index=4,
                key="chart_type_selector",
                label_visibility="collapsed"
            )

        try:
<<<<<<< HEAD
            if chart_type == "Auto":
                fig = create_chart(results_df, st.session_state.question)
=======

            # Import chart creation function based on selection
            if chart_type == "Auto":
                fig = create_chart(
                    results_df,
                    st.session_state.question
                )
>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7
            else:
                import plotly.express as px
                numeric_cols = results_df.select_dtypes(include="number").columns.tolist()
                categorical_cols = results_df.select_dtypes(include="object").columns.tolist()
<<<<<<< HEAD

=======
                
>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7
                if not numeric_cols:
                    st.warning("No numeric columns available for charting")
                    fig = None
                else:
                    x_col = categorical_cols[0] if categorical_cols else numeric_cols[0]
                    y_col = numeric_cols[0]
<<<<<<< HEAD

=======
                    
>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7
                    if chart_type == "Bar":
                        fig = px.bar(results_df, x=x_col, y=y_col, color=x_col, title=st.session_state.question)
                    elif chart_type == "Line":
                        fig = px.line(results_df, x=x_col, y=y_col, title=st.session_state.question, markers=True)
                        fig.update_traces(line_shape="spline", line=dict(width=3), marker=dict(size=8))
                    elif chart_type == "Pie":
                        fig = px.pie(results_df, names=x_col, values=y_col, title=st.session_state.question)
                    elif chart_type == "Scatter":
                        fig = px.scatter(results_df, x=x_col, y=y_col, color=x_col if categorical_cols else None, title=st.session_state.question)
                        fig.update_traces(marker=dict(size=12, line=dict(width=1, color='White')), opacity=0.8)
                    else:
                        fig = create_chart(results_df, st.session_state.question)

            if fig:
<<<<<<< HEAD
                fig.update_layout(
                    font=dict(family="Inter, sans-serif"),
                    title_font=dict(size=18),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=60, l=20, r=20, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No suitable chart could be generated.")

        except Exception as e:
            st.warning(f"Chart generation failed: {str(e)}")
=======

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:

                st.info(
                    "No suitable chart could be generated."
                )

        except Exception as e:

            st.warning(
                f"Chart generation failed: {str(e)}"
            )

# Insights, download, query-details and footer removed per user request
>>>>>>> b3bf8147d3c230a9960da7d25a0498a3266af2b7
