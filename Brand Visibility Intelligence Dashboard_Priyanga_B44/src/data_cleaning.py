import pandas as pd

# ---------------------------
# LOAD DATA
# ---------------------------
csv_df = pd.read_csv("data/brand_dirty_dataset.csv")
api_df = pd.read_csv("data/api_data.csv")

# ---------------------------
# STANDARDIZE COLUMN NAMES
# ---------------------------
csv_df.columns = csv_df.columns.str.lower()
api_df.columns = api_df.columns.str.lower()

# Fix mismatches
api_df.rename(columns={"source": "platform"}, inplace=True)

# ---------------------------
# ENSURE SAME COLUMNS
# ---------------------------
required_cols = [
    'keyword','title','price','raw_price','rating',
    'reviews','platform','position','delivery','link','thumbnail'
]

for col in required_cols:
    if col not in csv_df.columns:
        csv_df[col] = None
    if col not in api_df.columns:
        api_df[col] = None

# ---------------------------
# MERGE DATA
# ---------------------------
df = pd.concat([csv_df, api_df], ignore_index=True)

# ---------------------------
# CLEAN PRICE
# ---------------------------
df['price'] = df['price'].astype(str).str.replace(r"[^\d.]", "", regex=True)
df['price'] = pd.to_numeric(df['price'], errors='coerce')

df['raw_price'] = pd.to_numeric(df['raw_price'], errors='coerce')

# ---------------------------
# CLEAN RATING & REVIEWS
# ---------------------------
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
df['reviews'] = pd.to_numeric(df['reviews'], errors='coerce')

# ---------------------------
# HANDLE MISSING VALUES
# ---------------------------
df['rating'].fillna(df['rating'].median(), inplace=True)
df['reviews'].fillna(0, inplace=True)
df['delivery'].fillna("Unknown", inplace=True)

# ---------------------------
# REMOVE INVALID VALUES
# ---------------------------
df = df[df['price'] > 0]
df = df[df['position'] > 0]

# ---------------------------
# REMOVE DUPLICATES
# ---------------------------
df.drop_duplicates(subset=['title', 'price'], inplace=True)

# ---------------------------
# CLEAN TEXT
# ---------------------------
df['title'] = df['title'].str.replace(r"[^\w\s]", "", regex=True)
df['platform'] = df['platform'].str.lower().str.strip()
df['keyword'] = df['keyword'].str.lower().str.strip()

# ---------------------------
# SAVE
# ---------------------------
df.to_csv("data/cleaned_data.csv", index=False)

print("✅ Data cleaned and saved")