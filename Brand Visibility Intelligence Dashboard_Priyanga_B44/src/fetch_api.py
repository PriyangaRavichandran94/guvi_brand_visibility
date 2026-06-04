import requests
import pandas as pd
import time

API_KEY = "c3f44a1ad39a72b073ec5d71c1746e714772fa89cafbdcb5d2008f11c13fea9a"

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
    "google": "mobile"
}

# ---------------------------
# KEYWORDS
# ---------------------------
KEYWORDS = [
    "iphone",
    "Samsung",
    "Xiaomi",
    "Nothing",
    "Motorola",
    "Oppo",
    "Vivo",
    "Nokia",
    "Google"
]

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
# SINGLE FETCH FUNCTION
# ---------------------------
def fetch_single_query(query):

    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "error" in data:
        print("❌ FULL API ERROR:", data["error"])
        return pd.DataFrame()

    results = data.get("shopping_results", [])
    rows = []

    for item in results:

        row = {
            "keyword": query,
            "category": map_category(query),  # ✅ CATEGORY ADDED HERE
            "title": item.get("title"),
            "price": item.get("price"),
            "extracted_price": item.get("extracted_price"),
            "raw_price": item.get("extracted_price"),
            "rating": item.get("rating"),
            "reviews": item.get("reviews"),
            "platform": item.get("source"),
            "position": item.get("position"),
            "delivery": item.get("delivery"),
            "link": item.get("product_link"),
            "thumbnail": item.get("thumbnail")
        }

        # INSTALLMENT
        installment = item.get("installment", {})
        if isinstance(installment, dict):
            row["installment_price"] = installment.get("extracted_price")
            row["installment_months"] = installment.get("period")
        else:
            row["installment_price"] = None
            row["installment_months"] = None

        # CURRENCY DETECTION
        price_str = str(item.get("price", ""))
        if "$" in price_str:
            row["currency"] = "USD"
        elif "₹" in price_str:
            row["currency"] = "INR"
        else:
            row["currency"] = "UNKNOWN"

        rows.append(row)

    return pd.DataFrame(rows)

# ---------------------------
# MULTI-KEYWORD FETCH
# ---------------------------
def fetch_all_keywords(keywords):

    all_data = []

    for kw in keywords:
        print(f"Fetching: {kw}")

        try:
            df = fetch_single_query(kw)

            if not df.empty:
                all_data.append(df)

            time.sleep(2)  # avoid rate limit

        except Exception as e:
            print(f"Error fetching {kw}: {e}")

    if not all_data:
        return pd.DataFrame()

    final_df = pd.concat(all_data, ignore_index=True)
    return final_df

# ---------------------------
# RUN
# ---------------------------
api_df = fetch_all_keywords(KEYWORDS)

if api_df.empty:
    print("❌ DataFrame is empty — nothing to save")
else:
    print("✅ Rows fetched:", len(api_df))
    api_df.to_csv("data/api_data.csv", index=False)
    print("✅ CSV saved successfully")

print("✅ Multi-category API data ready")