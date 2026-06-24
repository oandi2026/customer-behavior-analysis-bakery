import pandas as pd 
import plotly.express as px 
import streamlit as st 

st.title("📊 Bakery Customer Behavior Analysis") 

# =========================
# LOAD DATA
# =========================
sheet_id = "1uhxrhGQ6UHpw4Xx09PUgMtj32Ukg9P2VsMmKvx7pofM"
url = f"https://google.com{sheet_id}/gviz/tq?tqx=out:csv"
df = pd.read_csv(url) 

# =========================
# CLEANING
# =========================
# Convert column names to uppercase and strip whitespace
df.columns = [c.strip().upper() for c in df.columns] 

# Robust check for columns (handles underscores like QUESTION_TEXT vs QUESTION TEXT)
for col in ["QUESTION TEXT", "QUESTION_ID", "ANSWER", "COUNT"]:
    if col not in df.columns:
        df.rename(columns={c: col for c in df.columns if col.replace(" ", "_") == c}, inplace=True)

df["ANSWER"] = df["ANSWER"].astype(str).str.strip() 
df["COUNT"] = pd.to_numeric(df["COUNT"], errors="coerce") 
df = df.dropna(subset=["ANSWER", "COUNT"]) 

# =========================
# INSIGHT MAPPING
# =========================
insights = {
    "1a": """The chart shows that the majority of customers purchase bakery products for personal consumption. 
    This indicates that individual demand is the primary revenue driver. Affordable and convenient products 
    such as filled buns play a crucial role in sustaining this demand.""",
    "1b": """A significant portion of customers purchase products for family consumption, highlighting the importance 
    of shareable and household-friendly items. This suggests an opportunity to introduce bundle packages or 
    family-sized offerings.""",
    "1c": """Purchases made for others indicate that bakery products are also used in social settings. 
    While not the primary driver, this segment presents opportunities for gift packaging and 
    occasion-based promotions.""",
    "2a": """Taste remains a critical factor influencing customer decisions. High agreement levels suggest that 
    product flavor meets customer expectations, reinforcing the importance of maintaining quality consistency.""",
    "2b": """The pricing perception is generally positive, indicating that customers find the products affordable. 
    This aligns well with mass-market positioning and supports volume-driven sales strategies.""",
    "2c": """Customers show moderate satisfaction with product variety, suggesting room for expansion. 
    Introducing new flavors or seasonal items could enhance customer engagement and repeat purchases.""",
    "2d": """Availability plays a key role in customer satisfaction. Any gaps in stock could directly impact sales, 
    indicating the need for better inventory planning and supply chain management.""",
    "2e": """Convenient store location contributes positively to customer purchase decisions. 
    This reinforces the importance of strategic placement and accessibility in driving foot traffic.""",
    "2f": """Packaging is perceived adequately but not as a primary driver. Enhancing packaging design could 
    improve brand perception and support premium positioning or gifting use cases.""",
    "2g": """Customer awareness of promotions appears limited, suggesting that marketing efforts may not be fully 
    optimized. Strengthening promotional campaigns could significantly boost sales volume.""",
    "3a": """Purchase frequency indicates stable repeat behavior among customers. This suggests a loyal customer base, 
    which can be further leveraged through loyalty programs or targeted offers.""",
    "3b": """Overall satisfaction levels are high, indicating strong product-market fit. Maintaining product quality, 
    competitive pricing, and availability will be key to sustaining long-term growth."""
}

# =========================
# SIDEBAR FILTER
# =========================
list_question = df["QUESTION TEXT"].unique() 
pilihan_pertanyaan = st.sidebar.selectbox("Select Question:", list_question) 
df_filtered = df[df["QUESTION TEXT"] == pilihan_pertanyaan] 

# Safety check to prevent IndexError if the filtered dataframe is empty
if not df_filtered.empty:
    # Forced to lowercase to match the insights dictionary keys properly
    question_id = str(df_filtered["QUESTION_ID"].iloc[0]).strip().lower()
else:
    question_id = None

# =========================
# GROUPING
# =========================
df_bar = df_filtered.groupby("ANSWER")["COUNT"].sum().reset_index() 
order = ["Strongly Agree", "Agree", "Don't Know", "Disagree", "Strongly Disagree"] 
df_bar["ANSWER"] = pd.Categorical(df_bar["ANSWER"], categories=order, ordered=True) 
df_bar = df_bar.sort_values("ANSWER") 

# =========================
# CHART
# =========================
fig = px.bar( 
    df_bar, 
    x="ANSWER", 
    y="COUNT", 
    text="COUNT", 
    title=f"Distribution of Responses for: {pilihan_pertanyaan}", 
    color="ANSWER", 
    color_discrete_sequence=px.colors.qualitative.Pastel 
) 
fig.update_traces(textposition='inside') 
fig.update_layout(xaxis_title="Responses", yaxis_title="Total Count") 
st.plotly_chart(fig, use_container_width=True)

# =========================
# INSIGHT OUTPUT
# =========================
st.markdown("### 📈 Key Insight")

if question_id in insights:
    if question_id == "3b":
        st.success(insights[question_id])
    elif question_id in ["2d", "2g"]:
        st.warning(insights[question_id])
    else:
        st.info(insights[question_id])
else:
    st.info("Insight not available for this question ID.")
