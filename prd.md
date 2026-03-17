Mini AI Sales Prediction System – Engineer
📌 DESKRIPSI SINGKAT
Buat mini sistem untuk mengelola data penjualan, memprediksi status produk (Laris/Tidak Laris), dan menampilkannya di dashboard. Fokus pada code quality, system thinking, dan integrasi ML ke backend. UI & deployment tidak dinilai.


🛠 TECH STACK
Bagian	Teknologi
Frontend	React JS, JavaScript, UI library bebas
Backend	FastAPI
Machine Learning	Scikit-learn
Dataset	CSV (product_id, name, jumlah_penjualan, harga, diskon, status)
📋 SCOPE PEKERJAAN
1. System Design (½ halaman)
Diagram arsitektur + alur data

2. Backend API
POST /login (JWT dummy)

GET /sales (ambil data)

POST /predict (prediksi status)

Struktur rapi, error handling, dokumentasi

3. Machine Learning (Classification)
Input: jumlah_penjualan, harga, diskon

Output: Laris/Tidak

Preprocessing, training, evaluasi (accuracy), save model

4. Frontend React
Login sederhana

Dashboard: tabel data + form prediksi

Integrasi API

5. Dokumentasi (README.md)
Cara jalankan project

Design decision

Asumsi

📁 STRUKTUR PROJECT
text
project-root/
├── backend/
├── frontend/
├── ml/
├── data/
│   └── sales_data.csv
└── README.md