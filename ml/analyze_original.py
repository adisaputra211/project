import pandas as pd

df = pd.read_csv('data/sales_data.csv', sep=';')

print(f"=== Total Data: {len(df)} ===\n")

# Cek EXCEPTION: penjualan >= 81 tapi Tidak
exceptions_tidak = df[(df['jumlah_penjualan'] >= 81) & (df['status'] == 'Tidak')]
print(f"Tidak dengan penjualan >= 81: {len(exceptions_tidak)}")
if len(exceptions_tidak) > 0:
    print("\nSample:")
    print(exceptions_tidak[['jumlah_penjualan', 'harga', 'diskon', 'status']].head(10).to_string())

# Cek EXCEPTION: penjualan < 81 tapi Laris
exceptions_laris = df[(df['jumlah_penjualan'] < 81) & (df['status'] == 'Laris')]
print(f"\nLaris dengan penjualan < 81: {len(exceptions_laris)}")
if len(exceptions_laris) > 0:
    print("\nSample:")
    print(exceptions_laris[['jumlah_penjualan', 'harga', 'diskon', 'status']].head(10).to_string())

# Tampilkan range harga untuk penjualan di sekitar threshold
print("\n=== Analisis di Sekitar Threshold (75-85) ===")
around = df[df['jumlah_penjualan'].between(75, 85)]
print(around[['jumlah_penjualan', 'harga', 'diskon', 'status']].head(20).to_string())

print("\n=== Distribusi Harga per Status ===")
print(df.groupby('status')['harga'].describe())
