import pandas as pd
import plotly.express as px
import streamlit as st

st.title("📊 Bakery Customer Behavior Analysis")

# 1. Correct URL format for CSV export (using gviz/tq endpoint)
sheet_id = "1uhxrhGQ6UHpw4Xx09PUgMtj32Ukg9P2VsMmKvx7pofM"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
df = pd.read_csv(url)

# 2. Clean and convert column names to uppercase
df.columns = [c.strip().upper() for c in df.columns]
df["ANSWER"] = df["ANSWER"].astype(str).str.strip()
df["COUNT"] = pd.to_numeric(df["COUNT"], errors="coerce")
df = df.dropna(subset=["ANSWER", "COUNT"])

st.write("DATA LOADED:", df.shape)

# =========================
# INSIGHT MAPPING
# =========================
insights = {
    "1a": """Based on the distribution data above, it is evident that personal consumption is the primary driver for most buyers. This trend aligns with observations showing that affordable filled breads—particularly cheese and chocolate buns—are highly favored by consumers. Because these products are both highly sought-after and profitable, increasing their production capacity is strongly recommended to maximize revenue""",
    "1b": """Based on the calculation results above, it can be stated that all respondents consume bread with their families. Consumers eat plain bread in the morning as a rice substitute together, which presents an opportunity for companies to offer plain bread in various variations. Examples include family sizes, oval or rectangular shapes, varying densities, and different toppings or spreads like a sprinkle of sesame seeds, butter, and so on.""",
    "1c": """Respondents also purchase bread to serve to personal guests, ranking fourth after family consumption, personal consumption, and gifting. To increase sales in this segment, the company should offer more visually appealing and presentable products, such as adding decorative toppings like sweets or cherries.""",
    "2a": """asdf""",
    "2b": """The pricing perception is generally positive, indicating that customers find the products affordable. This aligns well with mass-market positioning and supports volume-driven sales strategies.""",
    "2c": """Customers show moderate satisfaction with product variety, suggesting room for expansion. Introducing new flavors or seasonal items could enhance customer engagement and repeat purchases.""",
    "2d": """Availability plays a key role in customer satisfaction. Any gaps in stock could directly impact sales, indicating the need for better inventory planning and supply chain management.""",
    "2e": """Convenient store location contributes positively to customer purchase decisions. This reinforces the importance of strategic placement and accessibility in driving foot traffic.""",
    "2f": """Packaging is perceived adequately but not as a primary driver. Enhancing packaging design could improve brand perception and support premium positioning or gifting use cases.""",
    "2g": """Customer awareness of promotions appears limited, suggesting that marketing efforts may not be fully optimized. Strengthening promotional campaigns could significantly boost sales volume.""",
    "3a": """Purchase frequency indicates stable repeat behavior among customers. This suggests a loyal customer base, which can be further leveraged through loyalty programs or targeted offers.""",
    "3b": """Overall satisfaction levels are high, indicating strong product-market fit. Maintaining product quality, competitive pricing, and availability will be key to sustaining long-term growth."""
}

# 3. Filter data based on Sidebar selection
list_question = df["QUESTION TEXT"].unique()
selected_question = st.sidebar.selectbox("Select Question:", list_question)
df_filtered = df[df["QUESTION TEXT"] == selected_question]

# 4. Group filtered data
df_bar = df_filtered.groupby("ANSWER")["COUNT"].sum().reset_index()
order = ["Strongly Agree", "Agree", "Don't Know", "Disagree", "Strongly Disagree"]
df_bar["ANSWER"] = pd.Categorical(df_bar["ANSWER"], categories=order, ordered=True)
df_bar = df_bar.sort_values("ANSWER")

st.write(f"DATA FOR: {selected_question}", df_bar)

st.write(f"DATA FOR: {selected_question}", df_bar)

# 5. Generate and Display Chart
fig = px.bar(
    df_bar,
    x="ANSWER",
    y="COUNT",
    text="COUNT",
    title=f"Distribution of Responses for: {selected_question}",
    color="ANSWER",
    color_discrete_sequence=px.colors.qualitative.Pastel
)
fig.update_traces(textposition='inside')
fig.update_layout(xaxis_title="Responses", yaxis_title="Total Count")
st.plotly_chart(fig, use_container_width=True)

# 6. Display Analysis Insight Automatically (FIXED LOGIC)
selected_insight = None

if not df_filtered.empty and "QUESTION ID" in df_filtered.columns:
    # 1. Look up the actual ID (e.g., '1a') matching the chosen text
    current_id = str(df_filtered["QUESTION ID"].iloc[0]).strip().lower()
    
    # 2. Match the cleaned ID directly against the dictionary keys
    for key, insight_text in insights.items():
        if key.lower().strip() == current_id:
            selected_insight = insight_text
            break

if selected_insight:
    st.subheader("💡 Analysis Insight")
    st.info(selected_insight)
else:
    st.subheader("💡 Analysis Insight")
    st.caption("No specific insight mapped for this question format.")





