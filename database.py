import sqlite3

def simpan_data(df):
    conn = sqlite3.connect("sales.db")
    df.to_sql("penjualan", conn, if_exists="replace", index=False)
    conn.close()