import pandas as pd
import plotly.express as px
import streamlit as st

st.title("📊 Bakery Customer Behavior Analysis")

# 1. Load data (Menggunakan link Google Sheets Anda yang sudah terbukti bekerja di Notebook)
url = "https://google.com"
df = pd.read_csv(url)

# 2. Atur urutan Skala Likert
likert_order = [
    "Strongly Agree",
    "Agree",
    "Don't Know",
    "Disagree",
    "Strongly Disagree"
]
df['ANSWER'] = pd.Categorical(df['ANSWER'], categories=likert_order, ordered=True)

# 3. Hitung total data (Agregasi)
df_bar = (
    df.groupby('ANSWER', observed=False)['COUNT']
    .sum()
    .reset_index()
)

# 4. Membuat Bar Chart Plotly
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

# 5. MENAMPILKAN KE STREAMLIT (Bagian pengganti fig.show())
st.plotly_chart(fig, use_container_width=True)
