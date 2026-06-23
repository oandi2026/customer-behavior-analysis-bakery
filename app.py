import pandas as pd
import plotly.express as px
import streamlit as st

st.title("📊 Bakery Customer Behavior Analysis")

url = "https://google.com"

# 1. Load data
df = pd.read_csv(url)

# 2. Bersihkan nama kolom (Ubah ke UPPERCASE)
df.columns = [c.strip().upper() for c in df.columns]

# 3. Bersihkan isi data kolom ANSWER dan COUNT
df["ANSWER"] = df["ANSWER"].astype(str).str.strip()
df["COUNT"] = pd.to_numeric(df["COUNT"], errors="coerce")
df = df.dropna(subset=["ANSWER", "COUNT"])

st.write("DATA LOADED:", df.shape)

# 4. Tambahkan FITUR FILTER agar grafik tidak menumpuk semua pertanyaan
# Mengambil daftar pertanyaan unik untuk dropdown di Sidebar
list_pertanyaan = df["QUESTION TEXT"].unique()
pilihan_pertanyaan = st.sidebar.selectbox("Pilih Pertanyaan:", list_pertanyaan)

# Filter data berdasarkan pilihan user
df_filtered = df[df["QUESTION TEXT"] == pilihan_pertanyaan]

# 5. Grouping data yang sudah difilter
df_bar = df_filtered.groupby("ANSWER")["COUNT"].sum().reset_index()

# 6. Urutkan berdasarkan skala Likert secara aman
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
