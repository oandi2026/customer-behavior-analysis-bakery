import pandas as pd
import plotly.express as px
import streamlit as st

st.title("📊 Bakery Customer Behavior Analysis")

# 1. Load data from Google Sheets
sheet_id = "1uhxrhGQ6UHpw4Xx09PUgMtj32Ukg9P2VsMmKvx7pofM"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"

df = pd.read_csv(url)

# 2. Clean data
df.columns = [c.strip().upper() for c in df.columns]

df["ANSWER"] = df["ANSWER"].astype(str).str.strip()
df["COUNT"] = pd.to_numeric(df["COUNT"], errors="coerce")
df = df.dropna(subset=["ANSWER", "COUNT"])

st.write("DATA LOADED:", df.shape)

# 3. Sidebar filter
list_question = df["QUESTION TEXT"].unique()
pilihan_pertanyaan = st.sidebar.selectbox("Select Question:", list_question)

df_filtered = df[df["QUESTION TEXT"] == pilihan_pertanyaan].copy()

# 4. Likert order (IMPORTANT)
order = [
    "Strongly Disagree",
    "Disagree",
    "Don't Know",
    "Agree",
    "Strongly Agree"
]

df_filtered["ANSWER"] = pd.Categorical(
    df_filtered["ANSWER"],
    categories=order,
    ordered=True
)

# 5. Group data
df_grouped = df_filtered.groupby("ANSWER")["COUNT"].sum().reset_index()
df_grouped = df_grouped.sort_values("ANSWER")

# 6. Insight (AUTO)
top_answer = df_grouped.loc[df_grouped["COUNT"].idxmax(), "ANSWER"]
top_value = df_grouped["COUNT"].max()

st.metric("Top Response", top_answer, top_value)

# 7. Convert to percentage (for Likert style)
total = df_grouped["COUNT"].sum()
df_grouped["PERCENT"] = (df_grouped["COUNT"] / total) * 100

# 8. Stacked Likert Chart
fig = px.bar(
    df_grouped,
    x="PERCENT",
    y=[" "]*len(df_grouped),  # single stacked bar
    color="ANSWER",
    orientation="h",
    text=df_grouped["PERCENT"].round(1).astype(str) + "%",
    color_discrete_map={
        "Strongly Disagree": "#d73027",
        "Disagree": "#fc8d59",
        "Don't Know": "#cccccc",
        "Agree": "#91cf60",
        "Strongly Agree": "#1a9850"
    },
    title=f"Customer Sentiment Distribution: {pilihan_pertanyaan}"
)

# 9. Clean layout
fig.update_traces(textposition="inside")

fig.update_layout(
    barmode="stack",
    xaxis_title="Percentage (%)",
    yaxis_title="",
    showlegend=True,
    template="simple_white",
    height=400
)

st.plotly_chart(fig, use_container_width=True)
