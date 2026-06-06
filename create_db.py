import os
import csv
import sqlite3

def init_db():
    retail_csv  = os.path.join("database", "retail_sales_dataset.csv")
    legacy_csv  = os.path.join("sample_data", "sales.csv")
    db_path     = os.path.join("database", "uploaded_data.db")

    conn   = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # ── Retail sales table (new dataset) ─────────────────────────────────────
    if os.path.exists(retail_csv):
        print(f"Loading {retail_csv} ...")
        rows = []
        with open(retail_csv, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                rows.append((
                    int(row["Transaction ID"]),
                    row["Date"],
                    row["Customer ID"],
                    row["Gender"],
                    int(row["Age"]),
                    row["Product Category"],
                    int(row["Quantity"]),
                    float(row["Price per Unit"]),
                    float(row["Total Amount"]),
                ))

        cursor.execute("DROP TABLE IF EXISTS retail_sales")
        cursor.execute("""
            CREATE TABLE retail_sales (
                transaction_id   INTEGER PRIMARY KEY,
                date             TEXT    NOT NULL,
                customer_id      TEXT    NOT NULL,
                gender           TEXT    NOT NULL,
                age              INTEGER NOT NULL,
                product_category TEXT    NOT NULL,
                quantity         INTEGER NOT NULL,
                price_per_unit   REAL    NOT NULL,
                total_amount     REAL    NOT NULL
            )
        """)
        cursor.executemany("""
            INSERT INTO retail_sales VALUES (?,?,?,?,?,?,?,?,?)
        """, rows)
        print(f"retail_sales: {len(rows)} rows loaded.")
    else:
        print(f"Skipping retail_sales — {retail_csv} not found.")

    # Legacy sales table removal – the application now uses only the `retail_sales` dataset.
    # The block that previously loaded `sales.csv` has been omitted.
    # If you need the old data in the future, re‑enable this section.

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
