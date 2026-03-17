import pandas as pd
import numpy as np

np.random.seed(42)
n = 1000

# Generate features dengan variasi realistis
jumlah_penjualan = np.random.randint(10, 300, n)
harga = np.random.randint(20000, 200000, n)
diskon = np.random.choice([0, 5, 10, 15, 20, 25, 30], n)

# Formula realistis: kombinasi penjualan, harga, dan diskon
# Produk Laris jika: (penjualan tinggi) ATAU (harga rendah + diskon besar)
score = (jumlah_penjualan * 0.6) + ((200000 - harga) / 1000 * 0.25) + (diskon * 2 * 0.15)
threshold = np.percentile(score, 70)  # Top 30% = Laris
status = np.where(score >= threshold, 'Laris', 'Tidak')

# Tambahkan noise (5% data diacak labelnya untuk simulasi real-world)
noise_idx = np.random.choice(n, int(n * 0.05), replace=False)
for idx in noise_idx:
    status[idx] = 'Tidak' if status[idx] == 'Laris' else 'Laris'

df = pd.DataFrame({
    'product_id': [f'P{i:04d}' for i in range(1, n+1)],
    'product_name': [f'Produk {i}' for i in range(1, n+1)],
    'jumlah_penjualan': jumlah_penjualan,
    'harga': harga,
    'diskon': diskon,
    'status': status
})

df.to_csv('data/sales_data.csv', sep=';', index=False)
print('Data saved to data/sales_data.csv!')
print(f'\nDistribusi: {pd.Series(status).value_counts().to_dict()}')
print(f'\nStatistik jumlah_penjualan per kelas:')
print(df.groupby('status')['jumlah_penjualan'].describe())
print(f'\nOverlap check:')
laris_min = df[df['status']=='Laris']['jumlah_penjualan'].min()
tidak_max = df[df['status']=='Tidak']['jumlah_penjualan'].max()
print(f'Laris min penjualan: {laris_min}')
print(f'Tidak max penjualan: {tidak_max}')
print(f'Ada overlap: {laris_min < tidak_max}')
