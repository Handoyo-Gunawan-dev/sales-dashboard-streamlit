import streamlit as st
import pandas as pd
from database import simpan_data

st.title("Dashboard Penjualan Sederhana")

file = st.file_uploader("Upload file", type=["csv", "xlsx"])

if file:
    # Baca file
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    # Cleaning sederhana
    df = df.dropna()
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # Preview
    st.write(df.head())

    # Cek kolom dulu (biar nggak error)
    st.write("Kolom tersedia:", df.columns)

    # Analisis
    if "total" in df.columns:
        st.subheader("Total Penjualan")
        st.write(df["total"].sum())
    else:
        st.warning("Kolom 'total' tidak ditemukan")

    if "produk" in df.columns and "qty" in df.columns:
        st.subheader("Produk Terlaris")
        top_produk = df.groupby("produk")["qty"].sum().sort_values(ascending=False)
        st.bar_chart(top_produk)
    else:
        st.warning("Kolom 'produk' atau 'qty' tidak ditemukan")

    # Simpan ke database
    if st.button("Simpan ke Database"):
        simpan_data(df)
        st.success("Data berhasil disimpan!")

else:
    st.info("Silakan upload file terlebih dahulu")

    