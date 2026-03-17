import pickle
import pandas as pd


with open('ml/model.pkl', 'rb') as f:
    model = pickle.load(f)


print('=== Feature Importance (Kontribusi terhadap prediksi) ===')
for feat, imp in zip(['jumlah_penjualan', 'harga', 'diskon'], model.feature_importances_):
    print(f'{feat}: {imp:.4f} ({imp*100:.1f}%)')

print('\n=== Test Prediksi dengan Berbagai Skenario ===')
test_cases = [
    {'jumlah_penjualan': 250, 'harga': 50000, 'diskon': 20},  
    {'jumlah_penjualan': 50, 'harga': 50000, 'diskon': 20},  
    {'jumlah_penjualan': 80, 'harga': 30000, 'diskon': 30},   
    {'jumlah_penjualan': 80, 'harga': 150000, 'diskon': 0}, 
]

for tc in test_cases:
    pred = model.predict([[tc['jumlah_penjualan'], tc['harga'], tc['diskon']]])
    print(f"Penjualan={tc['jumlah_penjualan']}, Harga={tc['harga']}, Diskon={tc['diskon']}% -> {pred[0]}")
