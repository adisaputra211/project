"""
Analyze data patterns to find optimal formula for status prediction
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

df = pd.read_csv('data/sales_data.csv', sep=';')
print(f"Total data: {len(df)} rows")
print(f"\nDistribusi status:")
print(df['status'].value_counts())

# Try different formulas and find the best one
X = df[['jumlah_penjualan', 'harga', 'diskon']].values

# Convert status to binary
y_binary = (df['status'] == 'Laris').astype(int)

print("\n=== Testing Different Formulas ===")

# Formula 1: Equal weights
score1 = (
    (df['jumlah_penjualan'] / df['jumlah_penjualan'].max()) * 0.4 +
    (1 - df['harga'] / df['harga'].max()) * 0.4 +
    (df['diskon'] / 100) * 0.2
)

# Formula 2: Higher weight on penjualan
score2 = (
    (df['jumlah_penjualan'] / df['jumlah_penjualan'].max()) * 0.6 +
    (1 - df['harga'] / df['harga'].max()) * 0.3 +
    (df['diskon'] / 100) * 0.1
)

# Formula 3: Include interaction terms
score3 = (
    (df['jumlah_penjualan'] / df['jumlah_penjualan'].max()) * 0.5 +
    (1 - df['harga'] / df['harga'].max()) * 0.35 +
    (df['diskon'] / 100) * 0.15 +
    (df['jumlah_penjualan'] * df['diskon']) / (df['jumlah_penjualan'].max() * 100) * 0.1
)

# Formula 4: Log transform for harga (more realistic price sensitivity)
score4 = (
    (df['jumlah_penjualan'] / df['jumlah_penjualan'].max()) * 0.5 +
    (1 - np.log(df['harga']) / np.log(df['harga'].max())) * 0.35 +
    (df['diskon'] / 100) * 0.15
)

formulas = [
    ('Equal weights (40/40/20)', score1),
    ('Higher penjualan (60/30/10)', score2),
    ('With interaction terms', score3),
    ('Log price transform', score4),
]

best_accuracy = 0
best_formula = None
best_threshold = None
best_pred = None

for name, score in formulas:
    # Try different thresholds
    for percentile in [30, 35, 40, 45]:
        threshold = np.percentile(score, percentile)
        pred = (score >= threshold).astype(int)
        
        # Calculate accuracy
        accuracy = (pred == y_binary).mean()
        
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_formula = name
            best_threshold = threshold
            best_pred = pred

print(f"\n=== Best Formula ===")
print(f"Formula: {best_formula}")
print(f"Threshold percentile: finding optimal...")
print(f"Best accuracy: {best_accuracy:.2%}")

# Now test with the best formula
best_score = None
for name, score in formulas:
    if name == best_formula:
        best_score = score
        break

# Find optimal threshold
print("\n=== Finding Optimal Threshold ===")
for percentile in range(25, 55, 5):
    threshold = np.percentile(best_score, percentile)
    pred = (best_score >= threshold).astype(int)
    accuracy = (pred == y_binary).mean()
    laris_pct = pred.mean() * 100
    print(f"Percentile {percentile}: Threshold={threshold:.3f}, Accuracy={accuracy:.2%}, Laris={laris_pct:.1f}%")
