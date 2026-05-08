import requests
import pandas as pd
import time

API_KEY = "c3f44a1ad39a72b073ec5d71c1746e714772fa89cafbdcb5d2008f11c13fea9a"

def fetch_data(keyword):
    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google_shopping",
        "q": keyword,
        "api_key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    products = []

    for item in data.get("shopping_results", []):
        products.append({
            "keyword": keyword,
            "title": item.get("title"),
            "price": item.get("price"),
            "raw_price": item.get("extracted_price"),
            "rating": item.get("rating"),
            "reviews": item.get("reviews"),
            "platform": item.get("source"),
            "position": item.get("position"),
            "delivery": item.get("delivery"),
            "link": item.get("link"),
            "thumbnail": item.get("thumbnail")
        })

    return pd.DataFrame(products)


keywords = ["iphone", "laptop", "shoes", "headphones"]

all_data = []

for k in keywords:
    print(f"Fetching {k}...")
    df = fetch_data(k)
    all_data.append(df)
    time.sleep(2)  # avoid rate limit

api_df = pd.concat(all_data, ignore_index=True)

api_df.to_csv("data/api_data.csv", index=False)

print("✅ API data saved")