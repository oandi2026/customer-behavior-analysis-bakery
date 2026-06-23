import pandas as pd
import plotly.express as px
import streamlit as st

st.title("📊 Bakery Customer Behavior Analysis")

url = "https://docs.google.com/spreadsheets/d/1uhxrhGQ6UHpw4Xx09PUgMtj32Ukg9P2VsMmKvx7pofM/edit?usp=sharing"

df = pd.read_csv(url)

df.columns = [c.strip().upper() for c in df.columns]

df["ANSWER"] = df["ANSWER"].astype(str).str.strip()
df["COUNT"] = pd.to_numeric(df["COUNT"], errors="coerce")
df = df.dropna(subset=["ANSWER", "COUNT"])

st.write("DATA LOADED:", df.shape)

list_question = df["QUESTION TEXT"].unique()
pilihan_pertanyaan = st.sidebar.selectbox("Pilih Pertanyaan:", list_question)

df_filtered = df[df["QUESTION TEXT"] == pilihan_pertanyaan]

# 5. Grouping data yang sudah difilter
df_bar = df_filtered.groupby("ANSWER")["COUNT"].sum().reset_index()

order = ["Strongly Agree", "Agree", "Don't Know", "Disagree", "Strongly Disagree"]
df_bar["ANSWER"] = pd.Categorical(df_bar["ANSWER"], categories=order, ordered=True)
df_bar = df_bar.sort_values("ANSWER")

st.write(f"DATA UNTUK: {pilihan_pertanyaan}", df_bar)

# 7. Pembuatan Chart (Memastikan sumbu X dan Y menggunakan HURUF BESAR)
fig = px.bar(
    df_bar,
    x="ANSWER",      # Wajib huruf besar sesuai nama kolom baru
    y="COUNT",       # Wajib huruf besar sesuai nama kolom baru
    text="COUNT",
    title=f"Distribution of Responses for: {pilihan_pertanyaan}",
    color="ANSWER",  # Memberi warna berbeda tiap pilihan jawaban
    color_discrete_sequence=px.colors.qualitative.Pastel
)

# Mempercantik tampilan layout chart
fig.update_traces(textposition='inside')
fig.update_layout(xaxis_title="Responses", yaxis_title="Total Count")

# 8. Tampilkan ke Streamlit
st.plotly_chart(fig, use_container_width=True)
