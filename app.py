import pandas as pd 
import plotly.express as px 
import streamlit as st 

# Set page configuration
st.set_page_config(page_title="Bakery Analysis", layout="wide")

st.title("📊 Bakery Customer Behavior Analysis") 

# 1. Fetch data directly from Google Sheets
sheet_id = "1uhxrhGQ6UHpw4Xx09PUgMtj32Ukg9P2VsMmKvx7pofM"
url = f"https://google.com{sheet_id}/gviz/tq?tqx=out:csv"

df = pd.read_csv(url) 

# 2. Clean data and standardize columns
df.columns = [c.strip().upper() for c in df.columns] 
df["ANSWER"] = df["ANSWER"].astype(str).str.strip() 
df["COUNT"] = pd.to_numeric(df["COUNT"], errors="coerce") 
df = df.dropna(subset=["ANSWER", "COUNT"]) 

# 3. Sidebar Selection
list_question = df["QUESTION TEXT"].unique() 
pilihan_pertanyaan = st.sidebar.selectbox("Select Question to Visualize:", list_question) 

df_filtered = df[df["QUESTION TEXT"] == pilihan_pertanyaan] 

# 4. Process data for the bar chart
df_bar = df_filtered.groupby("ANSWER")["COUNT"].sum().reset_index() 
order = ["Strongly Agree", "Agree", "Don't Know", "Disagree", "Strongly Disagree"] 
df_bar["ANSWER"] = pd.Categorical(df_bar["ANSWER"], categories=order, ordered=True) 
df_bar = df_bar.sort_values("ANSWER") 

# 5. Create layout splits
col1, col2 = st.columns([2, 1])

with col1:
    # Generate and display the Chart
    fig = px.bar( 
        df_bar, 
        x="ANSWER", 
        y="COUNT", 
        text="COUNT", 
        title=f"Distribution of Responses: {pilihan_pertanyaan}", 
        color="ANSWER", 
        color_discrete_sequence=px.colors.qualitative.Pastel 
    ) 
    fig.update_traces(textposition='inside') 
    fig.update_layout(xaxis_title="Responses", yaxis_title="Total Count", showlegend=False) 
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Display the raw data table for the selected item
    st.write(f"**Data Table:** {pilihan_pertanyaan}")
    st.dataframe(df_bar, use_container_width=True, hide_index=True)

# 6. Static Business Insights Section at the Bottom
st.markdown("---")
st.subheader("💡 Key Executive Insights")

tab1, tab2, tab3 = st.tabs(["🚀 Core Drivers", "👥 Target Audience", "📦 Product & Price"])

with tab1:
    st.markdown("""
    * **Quality Trumps All:** **94% of customers** demand a **Soft texture** over dense variations.
    * **Freshness & Identity:** **84%** prioritize product freshness, and **82%** stick strictly to a **Known brand**. 
    """)

with tab2:
    st.markdown("""
    * **The Ultimate Family Item:** **100% of respondents** state they buy these products for family consumption.
    * **Morning Routine:** **72%** utilize bakery items specifically as a **Substitute for breakfast**, while lunch replacement stays low at 34%.
    """)

with tab3:
    st.markdown("""
    * **Visual appeal:** **80% of customers** state that **Attractive packaging** influences their selection.
    * **Pricing Divergence:** The audience is deeply split on cost (**38% agree** it is expensive, **36% disagree**). This signals an opportunity to market separate budget and premium tiers.
    """)
