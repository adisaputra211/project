"""
Final tuning: Make price the DOMINANT factor.
Very high prices should almost always be "Tidak" regardless of sales.
"""
import pandas as pd
import numpy as np

np.random.seed(42)

df = pd.read_csv('data/sales_data.csv', sep=';')
print(f"Loaded {len(df)} rows")

# Normalize
norm_penjualan = df['jumlah_penjualan'] / df['jumlah_penjualan'].max()
norm_harga = df['harga'] / df['harga'].max()
norm_diskon = df['diskon'] / 100


price_tier = np.where(
    norm_harga > 0.7, 0,      
    np.where(
        norm_harga > 0.4, 0.3,  
        0.5                       
    )
)


sales_factor = norm_penjualan * 0.5


discount_factor = norm_diskon * 0.15

score = price_tier + sales_factor + discount_factor


noise = np.random.normal(0, 0.12, len(df))
score = score + noise

threshold = np.percentile(score, 30)
new_status = np.where(score >= threshold, 'Laris', 'Tidak')


df['status'] = new_status
df.to_csv('data/sales_data.csv', sep=';', index=False)
print("✓ Data saved")

# Verify
print(f"\n=== Distribution ===")
print(df['status'].value_counts())

# Check specific cases
print(f"\n=== Key Test Cases ===")
cases = df[
    ((df['jumlah_penjualan'] == 136) & (df['harga'] == 199187)) |
    ((df['jumlah_penjualan'] == 102) & (df['harga'] == 101714)) |
    ((df['jumlah_penjualan'] == 152) & (df['harga'] == 187496)) |
    ((df['jumlah_penjualan'] == 40) & (df['harga'] <= 35000))
]
print(cases[['jumlah_penjualan', 'harga', 'diskon', 'status']].to_string())

# Overlap
print(f"\n=== Overlap ===")
laris_min = df[df['status']=='Laris']['jumlah_penjualan'].min()
tidak_max = df[df['status']=='Tidak']['jumlah_penjualan'].max()
print(f"Laris min: {laris_min}, Tidak max: {tidak_max}, Overlap: {laris_min < tidak_max}")

# High sales + high price
print(f"\n=== High Sales (>120) + High Price (>180k) ===")
hh = df[(df['jumlah_penjualan'] > 120) & (df['harga'] > 180000)]
print(f"Total: {len(hh)}, Laris: {(hh['status']=='Laris').sum()}, Tidak: {(hh['status']=='Tidak').sum()}")
