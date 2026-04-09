import streamlit as st
import pandas as pd
from database import simpan_data

st.title("Dashboard Penjualan Sederhana")

file = st.file_uploader("Upload file", type=["csv", "xlsx"])

if file:
    # --- Baca file ---
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    # --- Cleaning ---
    df = df.dropna()
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # --- Preview ---
    st.subheader("Preview Data")
    st.write(df.head())

    # --- Info kolom ---
    st.write("Kolom tersedia:", df.columns)

    # --- Ringkasan ---
    st.subheader("Ringkasan Data")
    col1, col2 = st.columns(2)
    col1.metric("Jumlah Baris", df.shape[0])
    col2.metric("Jumlah Kolom", df.shape[1])

    # --- Filter ---
    if "produk" in df.columns:
        st.subheader("Filter Data")
        produk_list = df["produk"].unique()
        pilih_produk = st.selectbox("Pilih Produk", ["Semua"] + list(produk_list))

        if pilih_produk != "Semua":
            df = df[df["produk"] == pilih_produk]

    # --- Analisis ---
    if "total" in df.columns:
        st.subheader("Total Penjualan")
        total_penjualan = df["total"].sum()
        st.metric("Total Penjualan", f"Rp {total_penjualan:,.0f}")
    else:
        st.warning("Kolom 'total' tidak ditemukan")

    if "produk" in df.columns and "qty" in df.columns:
        st.subheader("Produk Terlaris")
        top_produk = (
            df.groupby("produk")["qty"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )
        st.bar_chart(top_produk)
    else:
        st.warning("Kolom 'produk' atau 'qty' tidak ditemukan")

    # --- Simpan ---
    if st.button("Simpan ke Database"):
        simpan_data(df)
        st.success(f"{len(df)} baris data berhasil disimpan!")

else:
    st.info("Silakan upload file terlebih dahulu")