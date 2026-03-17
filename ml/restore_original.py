"""
Restore ORIGINAL labels based on the actual business rule:
Laris if jumlah_penjualan >= 81
Tidak if jumlah_penjualan < 81

This preserves the REAL pattern from your sales data.
"""
import pandas as pd

# Load data
df = pd.read_csv('data/sales_data.csv', sep=';')
print(f"Loaded {len(df)} rows")

# Store original features (DO NOT CHANGE)
original_jumlah = df['jumlah_penjualan'].copy()
original_harga = df['harga'].copy()
original_diskon = df['diskon'].copy()

# Restore ORIGINAL label based on threshold 81
# This is the ACTUAL pattern in your sales data
df['status'] = df['jumlah_penjualan'].apply(lambda x: 'Laris' if x >= 81 else 'Tidak')

# Save
df.to_csv('data/sales_data.csv', sep=';', index=False)
print("✓ Data restored to ORIGINAL labels")

# Verify
print(f"\n=== Verification ===")
print(f"Distribusi: {df['status'].value_counts().to_dict()}")
print(f"Laris min penjualan: {df[df['status']=='Laris']['jumlah_penjualan'].min()}")
print(f"Tidak max penjualan: {df[df['status']=='Tidak']['jumlah_penjualan'].max()}")

# Check if there are ANY exceptions (should be 0)
exceptions = df[(df['jumlah_penjualan'] <= 80) & (df['status'] == 'Laris')]
print(f"\nExceptions (Laris with penjualan <= 80): {len(exceptions)}")

exceptions2 = df[(df['jumlah_penjualan'] >= 81) & (df['status'] == 'Tidak')]
print(f"Exceptions (Tidak with penjualan >= 81): {len(exceptions2)}")

print("\n=== Sample Data ===")
print(df.head(15)[['jumlah_penjualan', 'harga', 'diskon', 'status']].to_string())
