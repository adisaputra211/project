import pickle

with open('ml/model.pkl', 'rb') as f:
    model = pickle.load(f)

test_cases = [
    {'jumlah_penjualan': 136, 'harga': 199187, 'diskon': 25},
    {'jumlah_penjualan': 102, 'harga': 101714, 'diskon': 15},
    {'jumlah_penjualan': 152, 'harga': 187496, 'diskon': 20},
    {'jumlah_penjualan': 40, 'harga': 30000, 'diskon': 25},
]

print('=== Test Model dengan Data Riil ===')
for tc in test_cases:
    pred = model.predict([[tc['jumlah_penjualan'], tc['harga'], tc['diskon']]])
    print(f"Penjualan={tc['jumlah_penjualan']}, Harga={tc['harga']:,}, Diskon={tc['diskon']}% -> {pred[0]}")
