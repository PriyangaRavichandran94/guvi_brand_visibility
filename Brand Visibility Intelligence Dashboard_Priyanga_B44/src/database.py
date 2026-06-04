import sqlite3
import pandas as pd

conn = sqlite3.connect("data/brand.db")

df = pd.read_csv("data/final_dataset.csv")

# type fixes
df['is_emi'] = df['is_emi'].astype(int)
df['top_10'] = df['top_10'].astype(int)

# DROP OLD TABLE (IMPORTANT FIX)
conn.execute("DROP TABLE IF EXISTS products")

# CREATE NEW TABLE (UPDATED SCHEMA)
conn.execute("""
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT,
    category TEXT,
    title TEXT,
    final_price REAL,
    rating REAL,
    reviews REAL,
    platform TEXT,
    delivery TEXT,
    currency TEXT,
    is_emi INTEGER,
    link TEXT,
    brand TEXT,
    visibility_score REAL,
    price_range TEXT,
    rating_category TEXT,
    review_category TEXT,
    top_10 INTEGER,
    value_score REAL
)
""")

conn.commit()

# insert fresh data
df.to_sql("products", conn, if_exists="append", index=False)

conn.commit()
conn.close()

print("✅ Database rebuilt successfully")