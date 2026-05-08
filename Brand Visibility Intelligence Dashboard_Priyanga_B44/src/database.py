import sqlite3


def create_connection():
    conn = sqlite3.connect("data/brand.db")
    return conn


def create_table(conn):
    query = """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        brand TEXT,
        price REAL,
        rating REAL,
        platform TEXT,
        visibility_score REAL,
        price_category TEXT,
        discount_percent REAL
    )
    """
    conn.execute(query)
    conn.commit()


def insert_data(conn, df):
    df.to_sql("products", conn, if_exists="replace", index=False)
    print("✅ Data inserted into DB")