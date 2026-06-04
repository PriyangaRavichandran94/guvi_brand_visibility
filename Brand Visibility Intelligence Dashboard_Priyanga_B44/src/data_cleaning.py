import pandas as pd
import numpy as np

USD_TO_INR = 83  # replace with live API if needed

# ---------------------------
# CATEGORY MAP
# ---------------------------
CATEGORY_MAP = {
    "iphone": "mobile",
    "samsung": "mobile",
    "xiaomi": "mobile",
    "nothing": "mobile",
    "motorola": "mobile",
    "oppo": "mobile",
    "vivo": "mobile",
    "nokia": "mobile",
    "google": "mobile",
    "laptop": "electronics",
    "headphone": "electronics",
    "shoe": "fashion",
    "office chair": "office equipments"
}

# ---------------------------
# CATEGORY FUNCTION
# ---------------------------
def map_category(keyword):
    keyword = str(keyword).lower()

    for key in CATEGORY_MAP:
        if key in keyword:
            return CATEGORY_MAP[key]
    return "other"

# ---------------------------
# MAIN FUNCTION
# ---------------------------
def load_and_merge_data(csv_path, api_path):

    # ---------------------------
    # LOAD DATA
    # ---------------------------
    csv_df = pd.read_csv(csv_path)
    api_df = pd.read_csv(api_path)

    # ---------------------------
    # STANDARDIZE COLUMN NAMES
    # ---------------------------
    csv_df.columns = csv_df.columns.str.lower().str.strip()
    api_df.columns = api_df.columns.str.lower().str.strip()

    # Fix mismatch
    api_df.rename(columns={"source": "platform"}, inplace=True)

    # ---------------------------
    # ADD CATEGORY (IMPORTANT 🔥)
    # ---------------------------
    # CSV → generate category
    if 'category' not in csv_df.columns:
        csv_df['category'] = csv_df['keyword'].apply(map_category)

    # API → already has category, but fallback if missing
    if 'category' not in api_df.columns:
        api_df['category'] = api_df['keyword'].apply(map_category)

    # ---------------------------
    # REQUIRED COLUMNS
    # ---------------------------
    required_cols = [
        'keyword','category','title','price','raw_price','rating',
        'reviews','platform','position','delivery','link','thumbnail',
        'extracted_price','installment_price','installment_months','currency'
    ]

    # Ensure all columns exist
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
    # STEP 1: BASE PRICE PRIORITY
    # ---------------------------
    df['base_price'] = df['installment_price'].combine_first(df['extracted_price'])

    df['base_price'] = df['base_price'].fillna(
        df['price'].astype(str).str.replace(r"[^\d.]", "", regex=True)
    )

    df['base_price'] = pd.to_numeric(df['base_price'], errors='coerce')

    # ---------------------------
    # STEP 2: DETECT CURRENCY
    # ---------------------------
    def detect_currency(row):
        if pd.notna(row.get('currency')):
            return row['currency']

        price = str(row.get('price', ''))
        if "$" in price:
            return "USD"
        elif "₹" in price:
            return "INR"
        return "UNKNOWN"

    df['currency'] = df.apply(detect_currency, axis=1)

    # ---------------------------
    # STEP 3: CONVERT TO INR
    # ---------------------------
    df['price_inr'] = np.where(
        df['currency'] == "USD",
        df['base_price'] * USD_TO_INR,
        df['base_price']
    )


    # ---------------------------
    # STEP 4: EMI HANDLING
    # ---------------------------
    df['installment_months'] = pd.to_numeric(df['installment_months'], errors='coerce')
    df['is_emi'] = df['installment_months'].notna()
    df['installment_months'] = df['installment_months'].fillna(1)

    # ---------------------------
    # STEP 5: FINAL PRICE
    # ---------------------------
    df['final_price'] = df['price_inr'] * df['installment_months']

    # ---------------------------
    # CLEAN NUMERIC COLUMNS
    # ---------------------------
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['reviews'] = pd.to_numeric(df['reviews'], errors='coerce')
    df['position'] = pd.to_numeric(df['position'], errors='coerce')
    df['position'] = df['position'].fillna(999)  # default for CSV

    # ---------------------------
    # HANDLE MISSING VALUES
    # ---------------------------
    df['rating'].fillna(df['rating'].median(), inplace=True)
    df['reviews'].fillna(0, inplace=True)
    df['delivery'].fillna("Unknown", inplace=True)

    # ---------------------------
    # REMOVE INVALID ROWS
    # ---------------------------

    
    df = df[(df['final_price'] > 0) & (df['position'] > 0)]

    # ---------------------------
    # REMOVE DUPLICATES
    # ---------------------------
    df.drop_duplicates(subset=['title', 'final_price'], inplace=True)

    # ---------------------------
    # CLEAN TEXT
    # ---------------------------
    df['title'] = df['title'].str.replace(r"[^\w\s]", "", regex=True)
    df['platform'] = df['platform'].str.lower().str.strip()
    df['keyword'] = df['keyword'].str.lower().str.strip()
    df['category'] = df['category'].str.lower().str.strip()

    # ---------------------------
    # FINAL OUTPUT
    # ---------------------------
    final_cols = [
        'keyword','category','title','final_price','rating','reviews',
        'platform','delivery','currency','is_emi','link'
    ]

    df = df[final_cols]

    return df


# ---------------------------
# RUN PIPELINE
# ---------------------------
df = load_and_merge_data(
    "data/brand_dirty_dataset.csv",
    "data/api_data.csv"
)

df.to_csv("data/cleaned_data.csv", index=False)

print("✅ FINAL MERGED DATA WITH CATEGORY READY")