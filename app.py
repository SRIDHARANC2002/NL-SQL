import streamlit as st
import pandas as pd
import os

from database.dynamic_db import (
    create_database_from_dataframe,
    get_schema,
    get_row_count,
    get_column_names
)

from agent.sql_generator import (
    generate_sql,
    check_ollama_status
)

from agent.validator import validate_sql
from agent.sql_executor import execute_sql
from agent.chart_generator import create_chart
from agent.explanation_generator import explain_sql
# from agent.insight_generator import generate_insights


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="NL → SQL Analytics Agent",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

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
}

.dataset-summary-row {
    display: flex;
    flex-wrap: wrap;
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

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "dataset_loaded" not in st.session_state:
    st.session_state.dataset_loaded = False

if "schema" not in st.session_state:
    st.session_state.schema = ""

if "question" not in st.session_state:
    st.session_state.question = ""

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title"> NL → SQL Analytics Agent</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Upload CSV, Excel, or a SQLite database file and ask questions in plain English</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

# Sidebar welcome and system status
st.sidebar.markdown("### 👋 Welcome\n\nUpload your dataset and ask questions in plain English.")

st.sidebar.subheader("⚙️ System Status")

ollama_running, has_model, models = check_ollama_status()

if ollama_running and has_model:
    st.sidebar.success(" Ollama Connected")
else:
    st.sidebar.error("Ollama Not Available")

# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

st.sidebar.subheader("📂 Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Choose CSV, Excel, or SQLite DB File",
    type=["csv", "xlsx", "xls", "db", "sqlite", "sqlite3"]
)

if uploaded_file:

    try:

        filename = uploaded_file.name.lower()

        if filename.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            create_database_from_dataframe(df)

        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
            create_database_from_dataframe(df)

        elif filename.endswith((".db", ".sqlite", ".sqlite3")):
            os.makedirs("database", exist_ok=True)

            with open("database/uploaded_data.db", "wb") as db_file:
                db_file.write(uploaded_file.getbuffer())

            st.sidebar.success("SQLite database uploaded")
            st.session_state.dataset_loaded = True

        else:
            raise ValueError("Unsupported file type. Please upload CSV, Excel, or SQLite database files.")

        if "dataset_loaded" in st.session_state and st.session_state.dataset_loaded:
            schema = get_schema()
            st.session_state.schema = schema

        # Dataset preview removed per user request

    except Exception as e:

        st.error(
            f"Dataset Upload Failed: {str(e)}"
        )

        st.stop()

# --------------------------------------------------
# STOP IF NO DATASET
# --------------------------------------------------

if not st.session_state.dataset_loaded:

    st.info(
        "Please upload a CSV or Excel dataset to begin."
    )

    st.stop()
# --------------------------------------------------
# QUESTION INPUT
# --------------------------------------------------

st.subheader("Dataset Summary")

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
    </div>
    <div class="dataset-summary-row">
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

st.markdown(summary_html, unsafe_allow_html=True)

st.subheader("Ask Your Question")

question = st.text_input(
    "Enter your question",
    value="",
    placeholder="Example: Average salary by department"
)

generate_button = st.button(
    "Generate SQL & Analyze",
    use_container_width=True
)

# --------------------------------------------------
# RUN ANALYSIS
# --------------------------------------------------

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

    left_col, right_col = st.columns([1, 1], gap="small")

    with left_col:
        st.subheader("Result Summary")

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
            </thead>
            <tbody>
                <tr><td>Rows Returned</td><td>{len(results_df)}</td></tr>
                <tr><td>Columns Returned</td><td>{len(results_df.columns)}</td></tr>
                <tr><td>Numeric Fields</td><td>{numeric_count}</td></tr>
            </tbody>
        </table>
        """

        st.markdown(summary_html, unsafe_allow_html=True)

    with right_col:
        st.subheader("Query Results")

        if results_df.empty:

            st.warning(
                "No records returned."
            )

        else:

            # Convert dataframe to HTML table with same styling as summary
            html_table = results_df.to_html(
                classes='summary-table',
                border=0,
                index=False,
                justify='left'
            )
            
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
        with col2:
            chart_type = st.selectbox(
                "Chart Type",
                ["Bar", "Line", "Pie", "Scatter", "Auto"],
                index=4,
                key="chart_type_selector",
                label_visibility="collapsed"
            )

        try:

            # Import chart creation function based on selection
            if chart_type == "Auto":
                fig = create_chart(
                    results_df,
                    st.session_state.question
                )
            else:
                import plotly.express as px
                numeric_cols = results_df.select_dtypes(include="number").columns.tolist()
                categorical_cols = results_df.select_dtypes(include="object").columns.tolist()
                
                if not numeric_cols:
                    st.warning("No numeric columns available for charting")
                    fig = None
                else:
                    x_col = categorical_cols[0] if categorical_cols else numeric_cols[0]
                    y_col = numeric_cols[0]
                    
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