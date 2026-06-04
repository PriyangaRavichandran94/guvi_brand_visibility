import pandas as pd
import sqlite3

conn = sqlite3.connect("data/brand.db")

df = pd.read_sql("SELECT * FROM products where category ='mobile' LIMIT 5", conn)

print(df)

conn.close()