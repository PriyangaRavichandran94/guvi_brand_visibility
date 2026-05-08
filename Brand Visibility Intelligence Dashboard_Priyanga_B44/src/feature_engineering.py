import pandas as pd
import numpy as np

df = pd.read_csv("data/cleaned_data.csv")

# ---------------------------
# BRAND
# ---------------------------
df['brand'] = df['title'].str.split().str[0]

# ---------------------------
# DISCOUNT
# ---------------------------
df['discount'] = ((df['raw_price'] - df['price']) / df['raw_price']) * 100
df['discount'] = df['discount'].fillna(0)

# ---------------------------
# VISIBILITY SCORE
# ---------------------------
df['visibility_score'] = 1 / df['position']

# ---------------------------
# PRICE RANGE
# ---------------------------
def price_bucket(x):
    if x < 500:
        return "Low"
    elif x < 2000:
        return "Medium"
    else:
        return "High"

df['price_range'] = df['price'].apply(price_bucket)

# ---------------------------
# RATING CATEGORY
# ---------------------------
df['rating_category'] = pd.cut(
    df['rating'],
    bins=[0, 2, 4, 5],
    labels=["Low", "Medium", "High"]
)

# ---------------------------
# REVIEW CATEGORY
# ---------------------------
df['review_category'] = pd.cut(
    df['reviews'],
    bins=[0, 100, 1000, df['reviews'].max()],
    labels=["Low", "Medium", "High"]
)

# ---------------------------
# FLAGS
# ---------------------------
df['is_discounted'] = df['discount'] > 0
df['top_10'] = df['position'] <= 10

# ---------------------------
# VALUE SCORE
# ---------------------------
df['value_score'] = (df['rating'] * df['reviews']) / df['price']

# ---------------------------
# CLEANING FINAL TOUCH
# ---------------------------
df['platform'] = df['platform'].str.title()
df['keyword'] = df['keyword'].str.lower()

# ---------------------------
# SAVE
# ---------------------------
df.to_csv("data/final_dataset.csv", index=False)

print("✅ Final dataset ready")