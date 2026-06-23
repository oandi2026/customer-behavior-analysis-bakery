import pandas as pd
import plotly.express as px
import streamlit as st

st.title("📊 Bakery Customer Behavior Analysis")

# 🔥 HARD FIX URL
url = "https://docs.google.com/spreadsheets/d/1uhxrhGQ6UHpw4Xx09PUgMtj32Ukg9P2VsMmKvx7pofM/gviz/tq?tqx=out:csv"

df = pd.read_csv(url)

# 🔥 FORCE CLEAN (ini yang sering bikin gagal diam-diam)
df.columns = [c.strip().upper() for c in df.columns]

df["ANSWER"] = df["ANSWER"].astype(str).str.strip()
df["COUNT"] = pd.to_numeric(df["COUNT"], errors="coerce")

# 🔥 DROP DATA RUSAK (INI KUNCI)
df = df.dropna(subset=["ANSWER", "COUNT"])

# 🔥 CHECK CEPAT (kalau ini kosong = masalah data)
st.write("DATA LOADED:", df.shape)

# 🔥 AGGREGASI
df_bar = df.groupby("ANSWER")["COUNT"].sum().reset_index()

st.write("GROUPED DATA:", df_bar)

# 🔥 PAKSA ORDER LIKERT
order = ["Strongly Agree","Agree","Don't Know","Disagree","Strongly Disagree"]

df_bar["ANSWER"] = pd.Categorical(df_bar["ANSWER"], categories=order, ordered=True)
df_bar = df_bar.sort_values("ANSWER")

# 🔥 CHART
fig = px.bar(
    df_bar,
    x="ANSWER",
    y="COUNT",
    text="COUNT",
    title="Total Distribution of Responses"
)

st.plotly_chart(fig, width="stretch")
