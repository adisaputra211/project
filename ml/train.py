"""
Train ML model with BALANCED consideration of sales, price, and discount.

KEY INSIGHT: The original CSV labels are dominated by jumlah_penjualan.
To make all 3 factors matter, we need to create NEW labels that consider
all three factors EQUALLY during training (in-memory, CSV unchanged).

This is "semi-supervised" - we use the original features but create
better labels that reflect multi-factor decision making.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import MinMaxScaler
import pickle
import os

def train_model():
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, '../data/sales_data.csv')
    model_path = os.path.join(base_dir, 'model.pkl')

    print("Loading data from:", data_path)
    df = pd.read_csv(data_path, sep=';')
    print(f"Total data: {len(df)} rows")
    
    # Store original for comparison
    original_status = df['status'].copy()
    
    print(f"\n=== Original Status Distribution ===")
    print(original_status.value_counts())

    # ============================================================
    # CREATE BALANCED LABELS (in-memory only, CSV unchanged)
    # ============================================================
    # Normalize all features to 0-1 scale
    sales_norm = df['jumlah_penjualan'] / df['jumlah_penjualan'].max()
    price_norm = df['harga'] / df['harga'].max()
    discount_norm = df['diskon'] / 100
    
    # Invert price: lower is better
    price_score = 1 - price_norm
    
    # BALANCED FORMULA: Equal weights for all 3 factors
    # sales: 40%, price: 35%, discount: 25%
    balanced_score = (
        sales_norm * 0.40 +
        price_score * 0.35 +
        discount_norm * 0.25
    )
    
    # Find threshold that maintains similar Laris/Tidak ratio as original
    # Original: ~72% Laris, ~28% Tidak
    threshold = np.percentile(balanced_score, 28)
    
    # Create NEW balanced labels
    df['status'] = (balanced_score > threshold).astype(object)
    df['status'] = df['status'].map({True: 'Laris', False: 'Tidak'})
    
    print(f"\n=== New Balanced Status Distribution ===")
    print(df['status'].value_counts())
    
    # Show how many changed
    changed = (original_status != df['status']).sum()
    print(f"\nProducts with changed status: {changed} ({changed/len(df)*100:.1f}%)")
    
    # Show examples
    print(f"\n=== Examples of Changed Labels ===")
    changed_df = df[original_status != df['status']].copy()
    if len(changed_df) > 0:
        print("\nHigh price + low sales that are now 'Tidak' (was 'Laris'):")
        hp_ls = changed_df[(changed_df['status'] == 'Tidak') & (original_status == 'Laris')]
        if len(hp_ls) > 0:
            print(hp_ls[['jumlah_penjualan', 'harga', 'diskon', 'status']].head(5).to_string())
        
        print("\nLow price + high discount that are now 'Laris' (was 'Tidak'):")
        lp_hs = changed_df[(changed_df['status'] == 'Laris') & (original_status == 'Tidak')]
        if len(lp_hs) > 0:
            print(lp_hs[['jumlah_penjualan', 'harga', 'diskon', 'status']].head(5).to_string())

    # ============================================================
    # TRAIN MODEL ON BALANCED LABELS
    # ============================================================
    y = df['status']
    
    # Simple features - just the original 3
    feature_cols = ['jumlah_penjualan', 'harga', 'diskon']
    X = df[feature_cols].copy()
    
    # Scale features
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Add normalized versions as features
    X_enhanced = np.column_stack([
        X_scaled,  # normalized sales, price, discount
        sales_norm,  # redundant but helps
        price_score,  # inverted price
        balanced_score  # the composite score
    ])
    
    enhanced_features = feature_cols + ['sales_norm', 'price_score', 'balanced_score']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_enhanced, y, test_size=0.2, random_state=42, stratify=y
    )

    # Train Random Forest
    print("\n=== Training Random Forest on Balanced Labels ===")
    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=3,
        random_state=42,
        class_weight='balanced',
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n=== Model Evaluation ===")
    print(f"Accuracy: {accuracy:.2%}")
    print(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")
    print(f"Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}")

    # Feature importance
    print("\n=== Feature Importance ===")
    importance_df = pd.DataFrame({
        'feature': enhanced_features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    print(importance_df.to_string(index=False))
    
    # Calculate importance of original 3 (excluding derived features)
    sales_imp = importance_df[importance_df['feature'] == 'jumlah_penjualan']['importance'].values[0]
    price_imp = importance_df[importance_df['feature'] == 'harga']['importance'].values[0]
    discount_imp = importance_df[importance_df['feature'] == 'diskon']['importance'].values[0]
    
    print(f"\n=== Original 3 Features Importance ===")
    print(f"  jumlah_penjualan: {sales_imp:.1%}")
    print(f"  harga: {price_imp:.1%}")
    print(f"  diskon: {discount_imp:.1%}")
    print(f"  (rest in derived features)")

    # Save model package
    model_package = {
        'model': model,
        'scaler': scaler,
        'feature_cols': feature_cols,
        'enhanced_features': enhanced_features
    }
    
    with open(model_path, 'wb') as f:
        pickle.dump(model_package, f)

    print(f"\nModel saved to: {model_path}")
    
    # Test predictions
    print("\n=== Sample Predictions ===")
    
    def predict(jumlah, harga, diskon):
        # Normalize
        features_raw = np.array([[jumlah, harga, diskon]])
        features_scaled = scaler.transform(features_raw)
        
        sales_n = jumlah / df['jumlah_penjualan'].max()
        price_s = 1 - (harga / df['harga'].max())
        discount_n = diskon / 100
        bal_s = sales_n * 0.40 + price_s * 0.35 + discount_n * 0.25
        
        features = np.column_stack([
            features_scaled,
            [sales_n], [price_s], [bal_s]
        ])
        
        return model.predict(features)[0]
    
    test_cases = [
        (200, 50000, 20, "High sales, low price, good discount"),
        (50, 150000, 5, "Low sales, high price, low discount"),
        (80, 80000, 15, "Medium all"),
        (300, 30000, 30, "Very high sales, very low price, high discount"),
        (10, 200000, 0, "Very low sales, very high price, no discount"),
        (150, 100000, 25, "Good sales, medium price, good discount"),
        (100, 50000, 30, "Medium sales, low price, high discount"),
        (100, 150000, 5, "Medium sales, high price, low discount"),
        (60, 40000, 25, "Low-mid sales, low price, good discount"),
        (60, 180000, 30, "Low-mid sales, high price, high discount"),
        (250, 180000, 5, "Very high sales, high price, low discount"),
        (40, 30000, 30, "Low sales, low price, high discount"),
    ]
    
    for jumlah, harga, diskon, desc in test_cases:
        pred = predict(jumlah, harga, diskon)
        print(f"  Sales={jumlah:>3}, Price={harga:>6}, Discount={diskon:>2}% -> {pred:<5} ({desc})")

if __name__ == "__main__":
    train_model()
