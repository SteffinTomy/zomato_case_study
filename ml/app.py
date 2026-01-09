from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib

# ============================================================
# HOW TO RUN THIS APPLICATION
# ============================================================
# 1. run:
#    uvicorn ml.app:app --reload
#
# 2. Open browser and go to:
#    http://127.0.0.1:8000/docs
#
# 3. Use the /predict endpoint and paste sample input
# ============================================================


# ============================================================
# LOAD MODEL & PREPROCESSING ARTIFACTS
# ============================================================
model = joblib.load("ml/rating_model.pkl")
scaler = joblib.load("ml/scaler.pkl")
feature_columns = joblib.load("ml/feature_columns.pkl")


# ============================================================
# FASTAPI APP INITIALIZATION
# ============================================================
app = FastAPI(
    title="Restaurant Rating Prediction API",
    description="Predicts restaurant ratings based on price, votes, and location details",
    version="1.0"
)


# ============================================================
# INPUT SCHEMA (VALIDATION)
# ============================================================
class RestaurantInput(BaseModel):
    price: float
    votes: int
    city: str
    region: str
    cuisine: str
    cuisine_type: str


# ============================================================
# PREDICTION ENDPOINT
# ============================================================
@app.post("/predict")
def predict_rating(data: RestaurantInput):
    """
    SAMPLE INPUT (copy-paste into Swagger UI):

    {
      "price": 500,
      "votes": 250,
      "city": "Bengaluru",
      "region": "Indiranagar",
      "cuisine": "North Indian",
      "cuisine_type": "Casual Dining"
    }
    """

    try:
        # Convert input to DataFrame
        df = pd.DataFrame([data.dict()])

        # -----------------------------
        # Feature Engineering
        # -----------------------------
        df["price_per_vote"] = df["price"] / (df["votes"] + 1)
        df["log_votes"] = np.log1p(df["votes"])

        # -----------------------------
        # One-hot encoding
        # -----------------------------
        df = pd.get_dummies(df)

        # Align columns with training data
        df = df.reindex(columns=feature_columns, fill_value=0)

        # -----------------------------
        # Scaling
        # -----------------------------
        df_scaled = scaler.transform(df)

        # -----------------------------
        # Prediction
        # -----------------------------
        prediction = model.predict(df_scaled)[0]

        return {
            "predicted_rating": round(float(prediction), 2)
        }

    except Exception as e:
        return {
            "error": "Prediction failed",
            "details": str(e)
        }
