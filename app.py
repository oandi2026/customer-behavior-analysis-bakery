import pandas as pd
import plotly.express as px
import streamlit as st

st.title("📊 Bakery Customer Behavior Analysis")

# Load data (WAJIB CSV valid)
url = "https://docs.google.com/spreadsheets/d/1uhxrhGQ6UHpw4Xx09PUgMtj32Ukg9P2VsMmKvx7pofM/gviz/tq?tqx=out:csv"
df = pd.read_csv(url)

# DEBUG
st.write(df.head())

likert_order = [
    "Strongly Agree",
    "Agree",
    "Don't Know",
    "Disagree",
    "Strongly Disagree"
]

df['ANSWER'] = pd.Categorical(df['ANSWER'], categories=likert_order, ordered=True)

df_bar = df.groupby('ANSWER', observed=False)['COUNT'].sum().reset_index()

fig = px.bar(
    df_bar,
    x="ANSWER",
    y="COUNT",
    color="ANSWER",
    title="Total Distribution of Responses",
    text="COUNT"
)

st.plotly_chart(fig, width='stretch')
