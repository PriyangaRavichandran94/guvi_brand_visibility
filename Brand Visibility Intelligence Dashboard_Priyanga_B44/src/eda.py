import pandas as pd

df = pd.read_csv("data/final_dataset.csv")

print("Shape:", df.shape)
print("\nData Types:\n", df.dtypes)

print("\nMissing %:\n", df.isnull().mean()*100)

# General
print("\nProducts per keyword:\n", df['keyword'].value_counts())
print("\nAvg price:", df['price'].mean())
print("\nPrice distribution:\n", df['price'].describe())
print("\nAvg rating:", df['rating'].mean())

# Brand
print("\nTop brands:\n", df['brand'].value_counts().head())
print("\nVisibility by brand:\n", df.groupby('brand')['visibility_score'].mean().sort_values(ascending=False).head())
print("\nAvg position by brand:\n", df.groupby('brand')['position'].mean())

# Pricing
print("\nPrice range distribution:\n", df['price_range'].value_counts())
print("\nAvg price per platform:\n", df.groupby('platform')['price'].mean())

# Discount
print("\n% discounted:", (df['discount'] > 0).mean()*100)
print("\nDiscount by brand:\n", df.groupby('brand')['discount'].mean())

# Platform
print("\nProducts per platform:\n", df['platform'].value_counts())
print("\nAvg rating per platform:\n", df.groupby('platform')['rating'].mean())

# Ranking
print("\nRanking distribution:\n", df['position'].describe())
print("\nTop products:\n", df.sort_values('position').head())