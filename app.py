import pandas as pd
import plotly.express as px
import streamlit as st

# Konfigurasi halaman utama
st.set_page_config(page_title="Bakery Customer Analytics", page_icon="📊", layout="wide")
st.title("📊 Bakery Customer Behavior Dashboard")
st.markdown("---")

# 1. Fungsi Load Data menggunakan Cache
@st.cache_data(ttl=3600)
def load_data():
    sheet_id = "1uhxrhGQ6UHpw4Xx09PUgMtj32Ukg9P2VsMmKvx7pofM"
    url = f"https://google.com{sheet_id}/gviz/tq?tqx=out:csv"
    try:
        data = pd.read_csv(url)
        data.columns = [c.strip().upper() for c in data.columns]
        data["ANSWER"] = data["ANSWER"].astype(str).str.strip()
        data["COUNT"] = pd.to_numeric(data["COUNT"], errors="coerce")
        data = data.dropna(subset=["ANSWER", "COUNT"])
        return data
    except Exception as e:
        st.error(f"Gagal mengambil data dari Google Sheets. Error: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    
    # 2. Sidebar Selection
    st.sidebar.header("🎯 Filter Analisis")
    list_question = df["QUESTION TEXT"].unique()
    pilihan_pertanyaan = st.sidebar.selectbox("Pilih Pertanyaan:", list_question)
    
    # Filter data berdasarkan pilihan
    df_filtered = df[df["QUESTION TEXT"] == pilihan_pertanyaan]
    
    # 3. Aggregation & Reindexing
    df_bar = df_filtered.groupby("ANSWER")["COUNT"].sum().reset_index()
    
    order = ["Strongly Agree", "Agree", "Don't Know", "Disagree", "Strongly Disagree"]
    df_bar["ANSWER"] = pd.Categorical(df_bar["ANSWER"], categories=order, ordered=True)
    df_bar = df_bar.sort_values("ANSWER").reset_index(drop=True)
    
    # Kalkulasi Persentase
    total_responden = df_bar["COUNT"].sum()
    df_bar["PERCENTAGE"] = (df_bar["COUNT"] / total_responden * 100).round(1) if total_responden > 0 else 0
    df_bar["LABEL"] = df_bar["COUNT"].astype(str) + " (" + df_bar["PERCENTAGE"].astype(str) + "%)"

    # --- 4. PERHITUNGAN KPI & INSIGHTS ---
    # Cari nilai persentase masing-masing kategori untuk logika insight
    val_dict = dict(zip(df_bar["ANSWER"].astype(str), df_bar["PERCENTAGE"]))
    
    positive_score = val_dict.get("Strongly Agree", 0) + val_dict.get("Agree", 0)
    negative_score = val_dict.get("Strongly Disagree", 0) + val_dict.get("Disagree", 0)
    neutral_score = val_dict.get("Don't Know", 0)
    
    # Cari jawaban dengan jumlah vote terbanyak (Modus)
    if not df_bar.empty and total_responden > 0:
        idx_max = df_bar["COUNT"].idxmax()
        jawaban_dominan = df_bar.loc[idx_max, "ANSWER"]
        persen_dominan = df_bar.loc[idx_max, "PERCENTAGE"]
    else:
        jawaban_dominan = "N/A"
        persen_dominan = 0

    # --- 5. TAMPILAN INTERFACE ---
    
    # Kategori 1: KEY PERFORMANCE INDICATORS (KPI)
    st.subheader("📌 Key Performance Indicators (KPI)")
    kpi1, kpi2, kpi3 = st.columns(3)
    
    with kpi1:
        st.metric(label="Total Responden", value=f"{int(total_responden):,}")
    with kpi2:
        st.metric(label="Sentimen Positif (Agree + Strongly Agree)", value=f"{positive_score:.1f}%", delta="Target: >70%")
    with kpi3:
        st.metric(label="Sentimen Negatif (Disagree + Strongly Disagree)", value=f"{negative_score:.1f}%", delta="-", delta_color="inverse")
        
    st.markdown("---")

    # Kategori 2: LAYOUT UTAMA (INSIGHTS & CHART)
    col_left, col_right = st.columns([1, 1.5])
    
    with col_left:
        st.subheader("💡 Key Insights (Wawasan Otomatis)")
        
        # Kotak Insight Dinamis Berdasarkan Data
        st.markdown(f"**Pertanyaan yang dianalisis:** *\"{pilihan_pertanyaan}\"*")
        
        # Logika 1: Kondisi Mayoritas Positif
        if positive_score >= 60:
            st.success(
                f"🟢 **Hasil Sangat Positif!**\n\n"
                f"Mayoritas pelanggan ({positive_score:.1f}%) memberikan respon setuju/sangat setuju. "
                f"Ini menunjukkan aspek bakery Anda pada poin ini sudah bekerja dengan sangat baik di mata konsumen."
            )
        # Logika 2: Kondisi Mayoritas Negatif
        elif negative_score >= 40:
            st.error(
                f"🔴 **Butuh Perbaikan Segera!**\n\n"
                f"Tingkat ketidaksetujuan mencapai {negative_score:.1f}%. "
                f"Aspek ini merupakan *pain point* utama pelanggan. Direkomendasikan bagi tim manajemen bakery untuk segera melakukan evaluasi operasional."
            )
        # Logika 3: Kondisi Berimbang / Netral Tinggi
        else:
            st.warning(
                f"🟡 **Hasil Cenderung Beragam / Netral**\n\n"
                f"Tidak ada sentimen dominan yang mutlak. Jawaban terbanyak adalah **{jawaban_dominan}** ({persen_dominan:.1f}%). "
                f"Konsumen tampak ragu-ragu atau memiliki pengalaman yang berbeda-beda terkait poin pertanyaan ini."
            )
            
        # Detail Tambahan Ringkas
        st.markdown("##### 📊 Fakta Angka:")
        st.write(f"- Dominasi Jawaban: **{jawaban_dominan}** dengan porsi **{persen_dominan}%**.")
        st.write(f"- Rasio Puas vs Tidak Puas: **{positive_score:.1f}%** berbanding **{negative_score:.1f}%**.")

        # Tombol Expand untuk melihat tabel mentah
        with st.expander("🔍 Lihat Detail Tabel Data"):
            st.dataframe(df_bar[["ANSWER", "COUNT", "PERCENTAGE"]], use_container_width=True, hide_index=True)

    with col_right:
        st.subheader("📊 Visualisasi Distribusi Jawaban")
        
        # Pembuatan Grafik Plotly
        fig = px.bar(
            df_bar,
            x="ANSWER",
            y="COUNT",
            text="LABEL",
            color="ANSWER",
            # Menggunakan mapping warna custom agar visualisasi lebih intuitif sesuai skala
            color_discrete_map={
                "Strongly Agree": "#2ca02c",   # Hijau Tua
                "Agree": "#98df8a",            # Hijau Muda
                "Don't Know": "#ffbb78",        # Jingga/Kuning
                "Disagree": "#ff9896",          # Merah Muda
                "Strongly Disagree": "#d62728"  # Merah Tua
            }
        )
        
        fig.update_traces(textposition='inside', textfont_size=12, textfont_color="white")
        fig.update_layout(
            xaxis_title="Tanggapan Responden", 
            yaxis_title="Jumlah Responden (Orang)",
            showlegend=False,
            margin=dict(t=20, b=40, l=40, r=40),
            height=450
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
else:
    st.info("Silakan periksa kembali file Google Sheets atau koneksi internet Anda.")
