import streamlit as st
import pandas as pd
from database import simpan_data

# 1. Konfigurasi Awal
st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Dashboard Penjualan Sederhana")

file = st.file_uploader("Upload file CSV atau Excel", type=["csv", "xlsx"])

if file:
    # --- 2. Baca Data ---
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    # --- 3. Cleaning Manual (Langkah demi Langkah) ---
    
    # Kecilkan semua huruf di nama kolom agar mudah dipanggil
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    
    # Tentukan nama kolom target (sesuaikan dengan file train.csv Anda)
    nama_kolom_sales = "item_mrp"
    nama_kolom_tahun = "outlet_establishment_year"
    nama_kolom_item  = "item_type"

    # Proses Kolom Penjualan
    if nama_kolom_sales in df.columns:
        # Paksa jadi angka, yang kotor jadi NaN (kosong)
        df[nama_kolom_sales] = pd.to_numeric(df[nama_kolom_sales], errors='coerce')
        # Hapus baris yang penjualannya kosong
        df = df.dropna(subset=[nama_kolom_sales])
    
    # Proses Kolom Tahun
    if nama_kolom_tahun in df.columns:
        df[nama_kolom_tahun] = pd.to_numeric(df[nama_kolom_tahun], errors='coerce')

    # --- 4. Tampilan Metrik (Atas) ---
    st.subheader("🔍 Ringkasan Data")
    kolom1, kolom2 = st.columns(2)
    
    jumlah_baris = len(df)
    kolom1.metric("Jumlah Transaksi", f"{jumlah_baris:,} Baris")

    if nama_kolom_sales in df.columns:
        total_uang = df[nama_kolom_sales].sum()
        kolom2.metric("Total Penjualan", f"Rp {total_uang:,.0f}")

    st.markdown("---")

    # --- 5. Visualisasi Sederhana ---
    kiri, kanan = st.columns(2)

    with kiri:
        st.subheader("📅 Tren Penjualan per Tahun")
        if nama_kolom_tahun in df.columns and nama_kolom_sales in df.columns:
            # Kelompokkan data berdasarkan tahun, lalu jumlahkan penjualannya
            tren_tahunan = df.groupby(nama_kolom_tahun)[nama_kolom_sales].sum()
            st.line_chart(tren_tahunan)
        else:
            st.warning("Kolom tahun tidak ditemukan")

    with kanan:
        st.subheader("📦 Kategori Terlaris")
        if nama_kolom_item in df.columns and nama_kolom_sales in df.columns:
            # Kelompokkan berdasarkan item, ambil 10 teratas
            top_10_item = df.groupby(nama_kolom_item)[nama_kolom_sales].sum().sort_values(ascending=False).head(10)
            st.bar_chart(top_10_item)
        else:
            st.warning("Kolom item tidak ditemukan")

    # --- 6. Tabel Data & Tombol Simpan ---
    st.markdown("---")
    st.subheader("📄 Preview Data Terakhir")
    st.dataframe(df.head(10))

    if st.button("💾 Simpan Hasil ke Database"):
        berhasil = simpan_data(df)
        if berhasil:
            st.success("Data berhasil diamankan ke database!")
        else:
            st.error("Gagal menyimpan data.")

else:
    st.info("Silakan unggah file Anda untuk melihat dashboard.")