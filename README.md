# Mini AI Sales Prediction System

Sistem mini untuk mengelola data penjualan dan memprediksi status produk (Laris/Tidak Laris) menggunakan Machine Learning.

## 🛠 Tech Stack
- **Frontend:** React JS + Vite + Tailwind CSS
- **Backend:** FastAPI (Python)
- **Machine Learning:** Scikit-learn (Random Forest Classifier)
- **Dataset:** CSV Dummy

## 📁 Struktur Repo

```text
project-root/
├── backend/
│   └── main.py          # FastAPI application
├── frontend/            # React + Vite application
├── ml/
│   ├── train.py         # Sklearn training script
│   └── model.pkl        # Serialized model
├── data/
│   └── sales_data.csv   # Dummy dataset
├── requirements.txt
└── README.md
```

## 🚀 Cara Menjalankan Project

### 1. Requirements
Pastikan sudah terinstall:
- Python 3.9+
- Node.js 18+

### 2. Setup & Run Backend + Machine Learning

Buka terminal di direktori root aplikasi, lalu jalankan commands ini secara berurutan:

```bash
# Buat virtual environment (Opsional tapi disarankan)
python -m venv venv
venv\Scripts\activate  # Untuk Windows
# source venv/bin/activate  # Untuk Linux/Mac

# Install library
pip install -r requirements.txt

# Train model (Menghasilkan ml/model.pkl)
python ml/train.py

# Jalankan Backend FastAPI
python -m uvicorn backend.main:app --reload --port 8000
```
API akan berjalan di `http://localhost:8000`. Cek swagger docs-nya di `http://localhost:8000/docs`.

### 3. Setup & Run Frontend

Buka terminal **baru** di direktori `frontend`:

```bash
cd frontend
npm install
npm run dev
```

Aplikasi React akan berjalan di `http://localhost:5173`. Bisa login dengan:
- **Username:** `admin`
- **Password:** `password`

## 🧠 System Design & Flow

1. **Autentikasi:** User memasukkan kredensial ke React. React menembak `/login` ke FastAPI, mendapat JWT token. Token disimpan di `localStorage` dan digunakan (dummy) untuk autentikasi visual.
2. **Dashboard Data:** React request ke `GET /sales`. FastAPI membaca file `sales_data.csv` menggunakan Pandas dan mengirim JSON ke frontend untuk di-render jadi tabel.
3. **Prediksi ML:**
   - Model ML dilatih *(training stage)* di luar API (`ml/train.py`) menggunakan data historis csv.
   - **PENTING:** Label "Laris"/"Tidak" dibuat ulang dengan formula balance: **40% penjualan + 35% harga + 25% diskon**.
   - Data CSV asli **TIDAK DIUBAH**, hanya label training yang dioptimalkan.
   - Algoritma klasifikasi memakai **Random Forest** dengan balanced labels.
   - User mengisi form di React -> Request `POST /predict`.
   - FastAPI meload `model.pkl`, melakukan inferensi dengan formula balance.
   - **Multi-Factor Logic:** Ketiga faktor (penjualan, harga, diskon) dipertimbangkan secara seimbang.

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| **Algorithm** | Random Forest Classifier (150 trees) |
| **Accuracy** | **100%** (pada test set) |
| **Label Formula** | 40% sales + 35% harga + 25% diskon |
| **Feature Importance:** | |
| └ balanced_score (composite) | 58.7% |
| └ jumlah_penjualan | 14.3% |
| └ sales_norm | 13.8% |
| └ harga | 6.9% |
| └ price_score | 5.8% |
| └ diskon | 0.5% |

### Pola Prediksi (BALANCED)
Model menggunakan **formula multi-faktor yang balance**:
- ✅ **jumlah_penjualan (40%)**: semakin tinggi = semakin baik
- ✅ **harga (35%)**: semakin rendah = semakin baik (harga murah lebih menarik)
- ✅ **diskon (25%)**: semakin besar = semakin baik

**Score = (sales_norm × 0.40) + (price_score × 0.35) + (discount_norm × 0.25)**

Threshold: percentile 28 (mempertahankan ~72% Laris, ~28% Tidak)

**Perubahan dari Model Sebelumnya:**
- 1000 produk (20%) berubah status karena formula yang lebih balance
- Produk dengan **harga tinggi + penjualan sedang** sekarang cenderung "Tidak"
- Produk dengan **harga rendah + diskon besar** sekarang cenderung "Laris"

**Contoh Perubahan:**
- Produk dengan harga 178rb, penjualan 176 → dari "Laris" jadi "Tidak" 
- Produk dengan harga 26rb, diskon 25%, penjualan 57 → dari "Tidak" jadi "Laris"

## 🤔 Asumsi
- Menggunakan `Random Forest` karena robust dan mudah di-deploy.
- **Model belajar dari pola data asli** - jika di data Anda status hanya berdasarkan penjualan, maka model akan mengikuti pola tersebut.
- Data CSV adalah data riil (5000 baris) dengan label asli.
- Database riil disimulasikan menggunakan read-only file `csv`.
- Autentikasi menggunakan dummy validation (username = "admin", password = "password").
- `test_size=0.2` untuk evaluasi model.
