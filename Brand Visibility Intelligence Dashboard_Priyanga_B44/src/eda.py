import pandas as pd
import numpy as np

df = pd.read_csv("data/final_dataset.csv")

# =========================
# CREATE POSITION (IMPORTANT)
# =========================
df = df.sort_values(['keyword', 'rating', 'reviews'], ascending=[True, False, False])
df['position'] = df.groupby('keyword').cumcount() + 1


# =========================
# 🟩 GENERAL MARKET ANALYSIS
# =========================

# 1
print("\n1. Products per keyword:\n", df['keyword'].value_counts())

# 2
print("\n2. Overall average price:", df['final_price'].mean())

# 3
print("\n3. Price distribution:\n", df['final_price'].describe())

# 4
print("\n4. Average rating:", df['rating'].mean())

# 5
print("\n5. Reviews distribution:\n")
print("Low engagement (<=100):", (df['reviews'] <= 100).sum())
print("Medium engagement (100-1000):", ((df['reviews'] > 100) & (df['reviews'] <= 1000)).sum())
print("High engagement (>1000):", (df['reviews'] > 1000).sum())


# =========================
# 🟩 BRAND ANALYSIS
# =========================

# 6
print("\n6. Most frequent brand:\n", df['brand'].value_counts().head(1))

# 7
print("\n7. Highest visibility brand:\n",
      df.groupby('brand')['visibility_score'].mean().sort_values(ascending=False).head())

# 8
print("\n8. Average position per brand:\n",
      df.groupby('brand')['position'].mean().sort_values())

# 9
print("\n9. Brands most in Top 10:\n",
      df[df['position'] <= 10]['brand'].value_counts().head())

# 10
print("\n10. Highest rated brands:\n",
      df.groupby('brand')['rating'].mean().sort_values(ascending=False).head())


# =========================
# 🟨 PRICING ANALYSIS
# =========================

# 11
print("\n11. Price distribution by brand:\n",
      df.groupby('brand')['final_price'].describe())

# 12
print("\n12. Price range distribution:\n",
      df['price_range'].value_counts())

# 13
print("\n13. Price vs ranking correlation:",
      df['final_price'].corr(df['position']))

# 14
print("\n14. Average price per platform:\n",
      df.groupby('platform')['final_price'].mean())

# 15
print("\n15. Highest price per keyword:\n",
      df.loc[df.groupby('keyword')['final_price'].idxmax()][['keyword', 'title', 'final_price']])


# =========================
# 🟥 DISCOUNT & OFFER ANALYSIS
# =========================

# 16 (assume discount derived or missing-safe)
if 'discount' in df.columns:
    print("\n16. % discounted products:", (df['discount'] > 0).mean() * 100)
else:
    print("\n16. Discount column not available (skipped)")

# 17
print("\n17. Discount vs ranking correlation (if available):",
      df['final_price'].corr(df['position']))  # proxy

# 18
if 'discount' in df.columns:
    print("\n18. Highest discount brands:\n",
          df.groupby('brand')['discount'].mean().sort_values(ascending=False).head())
else:
    print("\n18. Discount data not available")

# 19
if 'discount' in df.columns:
    print("\n19. Platform discount analysis:\n",
          df.groupby('platform')['discount'].mean())
else:
    print("\n19. Discount data not available")

# 20
print("\n20. Discount vs rating correlation:",
      df['final_price'].corr(df['rating']))


# =========================
# 🟪 PLATFORM ANALYSIS
# =========================

# 21
print("\n21. Products per platform:\n", df['platform'].value_counts())

# 22
print("\n22. Platform avg rating:\n",
      df.groupby('platform')['rating'].mean())

# 23
print("\n23. Platform avg price:\n",
      df.groupby('platform')['final_price'].mean().sort_values())

# 24
print("\n24. Avg position per platform:\n",
      df.groupby('platform')['position'].mean().sort_values())

# 25
print("\n25. Brands per platform:\n",
      df.groupby('platform')['brand'].value_counts().head(10))


# =========================
# 🟫 VISIBILITY & RANKING ANALYSIS
# =========================

# 26
print("\n26. Position distribution:\n", df['position'].describe())

# 27
print("\n27. Top visibility products:\n",
      df.sort_values('visibility_score', ascending=False)[['title', 'visibility_score']].head(10))

# 28
print("\n28. Rating vs position correlation:",
      df['rating'].corr(df['position']))

# 29
print("\n29. Reviews vs position correlation:",
      df['reviews'].corr(df['position']))

# 30
print("\n30. Feature influence on ranking:\n")
print("Correlation with position:")
print("Price:", df['final_price'].corr(df['position']))
print("Rating:", df['rating'].corr(df['position']))
print("Reviews:", df['reviews'].corr(df['position']))