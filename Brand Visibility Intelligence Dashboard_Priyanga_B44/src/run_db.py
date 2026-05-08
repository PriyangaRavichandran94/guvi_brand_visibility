import sqlite3
import pandas as pd

df = pd.read_csv("data/final_dataset.csv")

conn = sqlite3.connect("data/brand.db")

# Drop table if exists
conn.execute("DROP TABLE IF EXISTS products")

df.to_sql("products", conn, index=False)

print("✅ Database ready")