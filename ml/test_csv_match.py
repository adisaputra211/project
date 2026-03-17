import pandas as pd
import pickle

df = pd.read_csv('data/sales_data.csv', sep=';')
with open('ml/model.pkl', 'rb') as f:
    model = pickle.load(f)


row = df[(df['jumlah_penjualan'] == 136) & (df['harga'] == 199187)]
if len(row) > 0:
    row = row.iloc[0]
    print(f'Data CSV: penjualan={row["jumlah_penjualan"]}, harga={row["harga"]}, diskon={row["diskon"]}, status={row["status"]}')
    pred = model.predict([[row['jumlah_penjualan'], row['harga'], row['diskon']]])
    print(f'Model predict: {pred[0]}')
else:
    print('Data not found')

row2 = df[(df['jumlah_penjualan'] == 102) & (df['harga'] == 101714)]
if len(row2) > 0:
    row2 = row2.iloc[0]
    print(f'\nData CSV: penjualan={row2["jumlah_penjualan"]}, harga={row2["harga"]}, diskon={row2["diskon"]}, status={row2["status"]}')
    pred2 = model.predict([[row2['jumlah_penjualan'], row2['harga'], row2['diskon']]])
    print(f'Model predict: {pred2[0]}')
else:
    print('Data not found')


row3 = df[(df['jumlah_penjualan'] == 152) & (df['harga'] == 187496)]
if len(row3) > 0:
    row3 = row3.iloc[0]
    print(f'\nData CSV: penjualan={row3["jumlah_penjualan"]}, harga={row3["harga"]}, diskon={row3["diskon"]}, status={row3["status"]}')
    pred3 = model.predict([[row3['jumlah_penjualan'], row3['harga'], row3['diskon']]])
    print(f'Model predict: {pred3[0]}')
else:
    print('Data not found')
