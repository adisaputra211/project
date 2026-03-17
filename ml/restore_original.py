"""
Restore ORIGINAL labels based on the actual business rule:
Laris if jumlah_penjualan >= 81
Tidak if jumlah_penjualan < 81

This preserves the REAL pattern from your sales data.
"""
import pandas as pd

df = pd.read_csv('data/sales_data.csv', sep=';')
print(f"Loaded {len(df)} rows")

original_jumlah = df['jumlah_penjualan'].copy()
original_harga = df['harga'].copy()
original_diskon = df['diskon'].copy()

df['status'] = df['jumlah_penjualan'].apply(lambda x: 'Laris' if x >= 81 else 'Tidak')


df.to_csv('data/sales_data.csv', sep=';', index=False)
print("✓ Data restored to ORIGINAL labels")


print(f"\n=== Verification ===")
print(f"Distribusi: {df['status'].value_counts().to_dict()}")
print(f"Laris min penjualan: {df[df['status']=='Laris']['jumlah_penjualan'].min()}")
print(f"Tidak max penjualan: {df[df['status']=='Tidak']['jumlah_penjualan'].max()}")


exceptions = df[(df['jumlah_penjualan'] <= 80) & (df['status'] == 'Laris')]
print(f"\nExceptions (Laris with penjualan <= 80): {len(exceptions)}")

exceptions2 = df[(df['jumlah_penjualan'] >= 81) & (df['status'] == 'Tidak')]
print(f"Exceptions (Tidak with penjualan >= 81): {len(exceptions2)}")

print("\n=== Sample Data ===")
print(df.head(15)[['jumlah_penjualan', 'harga', 'diskon', 'status']].to_string())
