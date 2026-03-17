from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import pickle
import os
import jwt
import datetime
import numpy as np
import warnings

warnings.filterwarnings('ignore', category=UserWarning)

app = FastAPI(title="Mini AI Sales Prediction System")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "dummy_secret_key"

class LoginRequest(BaseModel):
    username: str
    password: str

class PredictRequest(BaseModel):
    jumlah_penjualan: int
    harga: float
    diskon: float

@app.post("/login")
def login(request: LoginRequest):
    if request.username == "admin" and request.password == "password":
        expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        token = jwt.encode({"sub": request.username, "exp": expiration}, SECRET_KEY, algorithm="HS256")
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/sales")
def get_sales(page: int = 1, limit: int = 10):
    data_path = os.path.join(os.path.dirname(__file__), '../data/sales_data.csv')
    if not os.path.exists(data_path):
        return {"data": [], "total_pages": 0, "total_hits": 0}

    df = pd.read_csv(data_path, sep=';')
    total_hits = len(df)
    total_pages = (total_hits + limit - 1) // limit

    page = max(1, min(page, total_pages)) if total_pages > 0 else 1
    start = (page - 1) * limit
    end = start + limit

    paginated_data = df.iloc[start:end].to_dict(orient="records")

    return {
        "data": paginated_data,
        "total_pages": total_pages,
        "total_hits": total_hits,
        "current_page": page
    }

# Load ML Model
model_path = os.path.join(os.path.dirname(__file__), '../ml/model.pkl')
try:
    with open(model_path, 'rb') as f:
        model_package = pickle.load(f)
        ml_model = model_package['model']
        scaler = model_package['scaler']
        feature_cols = model_package['feature_cols']
        
    # Load data for normalization (needed for balanced score calculation)
    data_path = os.path.join(os.path.dirname(__file__), '../data/sales_data.csv')
    df_train = pd.read_csv(data_path, sep=';')
    max_sales = df_train['jumlah_penjualan'].max()
    max_harga = df_train['harga'].max()
except Exception as e:
    ml_model = None
    scaler = None
    feature_cols = None
    max_sales = None
    max_harga = None

@app.post("/predict")
def predict_status(request: PredictRequest):
    if ml_model is None:
        raise HTTPException(status_code=500, detail="Model is not trained/loaded.")

    jumlah = request.jumlah_penjualan
    harga = request.harga
    diskon = request.diskon
    
    # Normalize raw features
    features_raw = np.array([[jumlah, harga, diskon]])
    features_scaled = scaler.transform(features_raw)
    
    # Calculate normalized values for balanced score
    sales_n = jumlah / max_sales
    price_score = 1 - (harga / max_harga)
    discount_n = diskon / 100
    
    # Balanced score: 40% sales, 35% price, 25% discount
    balanced_score = sales_n * 0.40 + price_score * 0.35 + discount_n * 0.25
    
    # Build enhanced feature vector
    features = np.column_stack([
        features_scaled,
        [sales_n],
        [price_score],
        [balanced_score]
    ])
    
    prediction = ml_model.predict(features)

    return {"status": prediction[0]}
