# loads the csv file and saves the data into a sqlite database
# i used sqlite because it doesnt need any server setup, just a file

import pandas as pd
import sqlite3
import os

RAW_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "supermarket_sales.csv")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "sales.db")


def load_raw_csv():
    csv_path = os.path.abspath(RAW_CSV)

    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"CSV not found at: {csv_path}\n"
            "Run data/raw/generate_data.py first to create it."
        )

    df = pd.read_csv(csv_path)
    print(f"loaded {len(df)} rows from csv")
    return df


def save_to_sqlite(df, table_name="sales"):
    db_path = os.path.abspath(DB_PATH)

    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

    print(f"saved to sqlite: {db_path}")
    return db_path


def query_db(sql, db_path=None):
    if db_path is None:
        db_path = os.path.abspath(DB_PATH)

    conn = sqlite3.connect(db_path)
    result = pd.read_sql_query(sql, conn)
    conn.close()
    return result
