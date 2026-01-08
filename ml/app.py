from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib

# -----------------------------
# LOAD MODEL & ARTIFACTS
# -----------------------------
model = joblib.load("ml/rating_model.pkl")
scaler = joblib.load("ml/scaler.pkl")
feature_columns = joblib.load("ml/feature_columns.pkl")

app = FastAPI(
    title="Restaurant Rating Prediction API",
    description="Predicts restaurant ratings based on cost, votes, and location",
    version="1.0"
)

# -----------------------------
# INPUT SCHEMA (Validation)
# -----------------------------
class RestaurantInput(BaseModel):
    price: float
    votes: int
    city: str
    region: str
    cuisine: str
    cuisine_type: str


# -----------------------------
# PREDICTION ENDPOINT
# -----------------------------
@app.post("/predict")
def predict_rating(data: RestaurantInput):
    try:
        df = pd.DataFrame([data.dict()])

        # Feature engineering (same as training)
        df["price_per_vote"] = df["price"] / (df["votes"] + 1)
        df["log_votes"] = np.log1p(df["votes"])

        # One-hot encoding
        df = pd.get_dummies(df)

        # Align with training columns
        df = df.reindex(columns=feature_columns, fill_value=0)

        # Scaling
        df_scaled = scaler.transform(df)

        # Prediction
        prediction = model.predict(df_scaled)[0]

        return {
            "predicted_rating": round(float(prediction), 2)
        }

    except Exception as e:
        return {
            "error": str(e)
        }
