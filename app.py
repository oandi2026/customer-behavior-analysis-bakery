import pandas as pd
import plotly.express as px
import streamlit as st

st.title("📊 Bakery Customer Behavior Analysis")

# 🔥 FIX URL (pakai gviz, ini pasti jalan)
url = "https://docs.google.com/spreadsheets/d/1uhxrhGQ6UHpw4Xx09PUgMtj32Ukg9P2VsMmKvx7pofM/gviz/tq?tqx=out:csv"
df = pd.read_csv(url)

# 🔥 rapikan kolom (WAJIB karena data kamu uppercase)
df.columns = df.columns.str.strip().str.upper()

# 🔥 pastikan COUNT numerik
df["COUNT"] = pd.to_numeric(df["COUNT"], errors="coerce")

# 🔥 urutan Likert
likert_order = [
    "Strongly Agree",
    "Agree",
    "Don't Know",
    "Disagree",
    "Strongly Disagree"
]

df["ANSWER"] = df["ANSWER"].astype(str).str.strip()
df["ANSWER"] = pd.Categorical(df["ANSWER"], categories=likert_order, ordered=True)

# 🔥 agregasi
df_bar = df.groupby("ANSWER", observed=False)["COUNT"].sum().reset_index()

# 🔥 chart
fig = px.bar(
    df_bar,
    x="ANSWER",
    y="COUNT",
    color="ANSWER",
    text="COUNT",
    title="Total Distribution of Responses"
)

st.plotly_chart(fig, width="stretch")
