import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Brand Visibility Dashboard", layout="wide")
st.title("📊 Brand Visibility Intelligence Dashboard")

# ---------------------------
# LOAD CLEAN DATA
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/final_cleaned_data.csv")
    return df

df = load_data()

# ---------------------------
# SIDEBAR FILTERS
# ---------------------------
st.sidebar.header("🔍 Filters")

brands = st.sidebar.multiselect(
    "Select Brand",
    options=df["brand"].dropna().unique(),
    default=df["brand"].dropna().unique()[:5]
)

platforms = st.sidebar.multiselect(
    "Select Platform",
    options=df["platform"].dropna().unique(),
    default=df["platform"].dropna().unique()
)

filtered_df = df[
    (df["brand"].isin(brands)) &
    (df["platform"].isin(platforms))
]

# ---------------------------
# KPIs
# ---------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("📦 Total Products", len(filtered_df))
col2.metric("🏷️ Unique Brands", filtered_df["brand"].nunique())
col3.metric("💰 Avg Price", f"₹{round(filtered_df['price'].mean(), 2)}")
col4.metric("⭐ Avg Rating", round(filtered_df["rating"].mean(), 2))

st.divider()

# ---------------------------
# CHARTS
# ---------------------------
fig1 = px.bar(
    filtered_df["brand"].value_counts().rename_axis("brand").reset_index(name="count"),
    x="brand",
    y="count",
    title="Brand Presence"
)

fig2 = px.histogram(
    filtered_df,
    x="price",
    nbins=20,
    title="Price Distribution"
)
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.scatter(
    filtered_df,
    x="price",
    y="rating",
    color="brand",
    title="Price vs Rating"
)
st.plotly_chart(fig3, use_container_width=True)

# ---------------------------
# TABLE
# ---------------------------
st.subheader("📋 Product Data")
st.dataframe(filtered_df)

# ---------------------------
# INSIGHTS
# ---------------------------
st.subheader("🧠 Insights")

if not filtered_df.empty:
    top_brand = filtered_df["brand"].value_counts().idxmax()
    avg_price = round(filtered_df["price"].mean(), 2)

    st.success(f"Top Brand: {top_brand}")
    st.info(f"Average Price: ₹{avg_price}")

# ---------------------------
# DOWNLOAD
# ---------------------------
csv_download = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Data",
    data=csv_download,
    file_name="filtered_data.csv",
    mime="text/csv"
)