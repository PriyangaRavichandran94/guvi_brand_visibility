import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title=" Brand Dashboard",
    layout="wide"
)

# =========================
# STYLE (DARK AMAZON UI)
# =========================
st.markdown("""
<style>
.main { background-color: #d1bce8; color: white; }
h1, h2, h3 { color: #ff9900; }

.stMetric {
    background-color: #d1bce8;
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🛒Brand Visibility Dashboard")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("data/final_dataset.csv")

    # -------------------------
    # CLEANING (IMPORTANT)
    # -------------------------
    df = df.fillna({
        "reviews": 0,
        "rating": df["rating"].median(),
        "final_price": df["final_price"].median()
    })

    df["reviews"] = pd.to_numeric(df["reviews"], errors="coerce").fillna(0)
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(df["rating"].median())
    df["final_price"] = pd.to_numeric(df["final_price"], errors="coerce").fillna(df["final_price"].median())

    # -------------------------
    # ENGINEER POSITION
    # -------------------------
    df = df.sort_values(['keyword', 'rating', 'reviews'], ascending=[True, False, False])
    df['position'] = df.groupby('keyword').cumcount() + 1

    return df

df = load_data()

# =========================
# FILTERS (CLEAN UI)
# =========================
st.markdown("### 🔍 Filters")

col1, col2, col3, col4 = st.columns(4)

with col1:
    brand_filter = st.multiselect("Brand", sorted(df["brand"].dropna().unique()))

with col2:
    platform_filter = st.multiselect("Platform", sorted(df["platform"].dropna().unique()))

with col3:
    keyword_filter = st.multiselect("Keyword", sorted(df["keyword"].dropna().unique()))

with col4:
    position_filter = st.slider(
        "Position",
        int(df["position"].min()),
        int(df["position"].max()),
        (1, 50)
    )

# =========================
# FILTER LOGIC (SAFE)
# =========================
filtered_df = df.copy()

if brand_filter:
    filtered_df = filtered_df[filtered_df["brand"].isin(brand_filter)]

if platform_filter:
    filtered_df = filtered_df[filtered_df["platform"].isin(platform_filter)]

if keyword_filter:
    filtered_df = filtered_df[filtered_df["keyword"].isin(keyword_filter)]

filtered_df = filtered_df[
    filtered_df["position"].between(position_filter[0], position_filter[1])
]

# =========================
# TABS
# =========================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview",
    "🏷️ Brand Insights",
    "💰 Pricing",
    "📦 Platform",
    "📈 Visibility",
    "🔍 Product Explorer"
])

# =========================
# 1. OVERVIEW
# =========================
with tab1:
    st.subheader("Overview KPIs")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Products", len(filtered_df))
    c2.metric("Avg Price", f"₹{filtered_df['final_price'].mean():.2f}")
    c3.metric("Avg Rating", f"{filtered_df['rating'].mean():.2f}")
    c4.metric("Total Reviews", int(filtered_df['reviews'].sum()))

    fig1 = px.histogram(filtered_df, x="final_price", nbins=25, title="Price Distribution",color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig1, use_container_width=True)

    kw = filtered_df["keyword"].value_counts().reset_index()
    kw.columns = ["keyword", "count"]

    fig2 = px.bar(kw, x="keyword", y="count", title="Products per Keyword", color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig2, use_container_width=True)

fig3 = px.treemap(
    filtered_df,
    path=["platform"],
    title="Platform Share"
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# 2. BRAND INSIGHTS
# =========================
with tab2:
    st.subheader("Brand Insights")

    top_brand = filtered_df["brand"].value_counts().idxmax()
    st.metric("Top Brand", top_brand)
    st.metric("Avg Visibility", round(filtered_df["visibility_score"].mean(), 2))

    b1 = filtered_df["brand"].value_counts().reset_index()
    b1.columns = ["brand", "count"]

    fig1 = px.bar(b1, x="brand", y="count", title="Brand Count",color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig1)

    fig2 = px.bar(filtered_df.groupby("brand")["rating"].mean().reset_index(),
                  x="brand", y="rating",
                  title="Brand Avg Rating",color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig2)

    top10 = filtered_df[filtered_df["position"] <= 10]["brand"].value_counts().reset_index()
    top10.columns = ["brand", "count"]

    fig3 = px.bar(top10, x="brand", y="count", title="Top Brands in Top 10",color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig3)

# =========================
# 3. PRICING
# =========================
with tab3:
    st.subheader("Pricing Analysis")

    c1, c2 = st.columns(2)
    c1.metric("Avg Price", f"₹{filtered_df['final_price'].mean():.2f}")
    c2.metric("Max Price", f"₹{filtered_df['final_price'].max():.2f}")

    fig1 = px.histogram(filtered_df, x="final_price", nbins=25,color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig1)

    fig2 = px.scatter(filtered_df, x="final_price", y="position", color="brand")
    st.plotly_chart(fig2)

    fig3 = px.scatter(filtered_df, x="final_price", y="rating", color="brand")
    st.plotly_chart(fig3)

# =========================
# 4. PLATFORM
# =========================
with tab4:
    st.subheader("Platform Analysis")

    c1, c2 = st.columns(2)
    c1.metric("Platforms", filtered_df["platform"].nunique())
    c2.metric("Best Platform", filtered_df.groupby("platform")["rating"].mean().idxmax())

    p1 = filtered_df["platform"].value_counts().reset_index()
    p1.columns = ["platform", "count"]

    fig1 = px.bar(p1, x="platform", y="count")
    st.plotly_chart(fig1)

    fig2 = px.bar(filtered_df.groupby("platform")["final_price"].mean().reset_index(),
                  x="platform", y="final_price")
    st.plotly_chart(fig2)

    fig3 = px.bar(filtered_df.groupby("platform")["rating"].mean().reset_index(),
                  x="platform", y="rating")
    st.plotly_chart(fig3)

# =========================
# 5. VISIBILITY
# =========================
with tab5:
    st.subheader("Visibility & Ranking")

    c1, c2 = st.columns(2)
    c1.metric("Avg Position", round(filtered_df["position"].mean(), 2))
    c2.metric("Avg Visibility", round(filtered_df["visibility_score"].mean(), 2))

    fig1 = px.histogram(filtered_df, x="position")
    st.plotly_chart(fig1)

    fig2 = px.scatter(filtered_df, x="rating", y="position")
    st.plotly_chart(fig2)

    fig3 = px.scatter(filtered_df, x="reviews", y="position", size="reviews")
    st.plotly_chart(fig3)

# =========================
# 6. PRODUCT EXPLORER
# =========================
with tab6:
    st.subheader("Product Explorer")

    search = st.text_input("Search Product Title")

    temp = filtered_df.copy()

    if search:
        temp = temp[temp["title"].str.contains(search, case=False)]

    st.dataframe(
        temp.sort_values("position")[
            ["title", "brand", "final_price", "rating",
             "reviews", "platform", "position"]
        ],
        use_container_width=True
    )