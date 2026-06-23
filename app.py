import pandas as pd
import plotly.express as px
import streamlit as st

st.title("📊 Likert Survey Analysis")

# Load data
url = "https://docs.google.com/spreadsheets/d/1uhxrhGQ6UHpw4Xx09PUgMtj32Ukg9P2VsMmKvx7pofM/export?format=csv"
df = pd.read_csv(url)

# Likert order
likert_order = [
    "Strongly Agree",
    "Agree",
    "Don't Know",
    "Disagree",
    "Strongly Disagree"
]

df['ANSWER'] = pd.Categorical(df['ANSWER'], categories=likert_order, ordered=True)

# Aggregation
df_bar = (
    df.groupby('ANSWER', observed=False)['COUNT']
    .sum()
    .reset_index()
)

# Chart
fig = px.bar(
    df_bar,
    x="ANSWER",
    y="COUNT",
    color="ANSWER",
    title="Total Distribution of Responses",
    text="COUNT"
)

fig.update_layout(
    xaxis_title="Skala Respon",
    yaxis_title="Total Count"
)

# Show in Streamlit
st.plotly_chart(fig, width='stretch')
