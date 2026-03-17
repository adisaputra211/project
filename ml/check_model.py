import pickle

with open('ml/model.pkl', 'rb') as f:
    model = pickle.load(f)

print('=== Feature Importance ===')
for feat, imp in zip(['jumlah_penjualan', 'harga', 'diskon'], model.feature_importances_):
    print(f'{feat}: {imp:.4f} ({imp*100:.1f}%)')

# Test prediksi
print('\n=== Test Prediksi ===')
test_cases = [
    [250, 50000, 20],
    [50, 50000, 20],
    [80, 30000, 30],
    [80, 150000, 0],
    [102, 100000, 15],  # Kasus yang Anda sebutkan
]

for tc in test_cases:
    pred = model.predict([tc])
    print(f'Penjualan={tc[0]}, Harga={tc[1]}, Diskon={tc[2]}% -> {pred[0]}')
