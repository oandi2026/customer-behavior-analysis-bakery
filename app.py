import pandas as pd
import plotly.express as px
import streamlit as st

# Tampilan judul web Streamlit
st.title("Bakery Customer Behavior Analysis")

# Load data
url = "https://google.com"
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

# Aggregate total count per answer
df_bar = (
    df.groupby('ANSWER', observed=False)['COUNT']
    .sum()
    .reset_index()
)

# Bar chart (Pastikan bagian variabel "fig" ini ada dan tidak terhapus)
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

# Menampilkan grafik ke dalam dashboard Streamlit
st.plotly_chart(fig, use_container_width=True)
