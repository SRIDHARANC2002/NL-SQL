import os
import sqlite3
import pandas as pd
import pytest
from plotly.graph_objs import Figure

# Import known agent modules
from agent.validator import validate_sql
from agent.chart_generator import create_chart

TEST_DB_PATH = "database/test_sales.db"

# ── Fixtures ──────────────────────────────────────────────────────────────────
@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    """Setup a temporary database for testing."""
    os.makedirs(os.path.dirname(TEST_DB_PATH), exist_ok=True)
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()

    # Create dummy sales table
    cursor.execute("DROP TABLE IF EXISTS sales")
    cursor.execute("""
        CREATE TABLE sales (
            id INTEGER PRIMARY KEY,
            product_category TEXT,
            revenue REAL,
            region TEXT
        )
    """)
    cursor.executemany(
        "INSERT INTO sales (product_category, revenue, region) VALUES (?, ?, ?)",
        [("Electronics", 1500, "North"), ("Clothing", 500, "South"), ("Electronics", 2000, "West")]
    )
    conn.commit()
    conn.close()

# ── Validator Tests ───────────────────────────────────────────────────────────
class TestValidator:
    def test_valid_select(self):
        assert validate_sql("SELECT * FROM sales;") == True

    def test_invalid_drop(self):
        assert validate_sql("DROP TABLE sales;") == False

    def test_invalid_update(self):
        assert validate_sql("UPDATE sales SET revenue=0;") == False

# ── Chart Generator Tests ─────────────────────────────────────────────────────
class TestChartGenerator:
    def test_create_chart_returns_figure(self):
        df = pd.DataFrame({
            "product_category": ["Electronics", "Clothing", "Home", "Beauty"],
            "revenue": [5000, 3000, 4000, 2500]
        })
        question = "Total revenue by product category"
        fig = create_chart(df, question)
        assert isinstance(fig, Figure)
        assert fig.layout.title.text is not None

    def test_create_chart_empty_dataframe(self):
        df = pd.DataFrame()
        fig = create_chart(df, "Empty data")
        assert fig is None
