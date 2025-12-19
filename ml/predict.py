import pandas as pd
import numpy as np
import joblib

# -----------------------------
# 1. LOAD SAVED MODEL & TOOLS
# -----------------------------
model = joblib.load("ml/rating_model.pkl")
scaler = joblib.load("ml/scaler.pkl")
feature_columns = joblib.load("ml/feature_columns.pkl")

print("Model and preprocessing artifacts loaded successfully.")

# -----------------------------
# 2. NEW RESTAURANT INPUT
# -----------------------------
new_restaurant = {
    "price": 500,
    "votes": 250,
    "city": "Bengaluru",
    "region": "Indiranagar",
    "cuisine": "North Indian",
    "cuisine_type": "Casual Dining"
}

df = pd.DataFrame([new_restaurant])

print("\nInput data:")
print(df)

# -----------------------------
# 3. FEATURE ENGINEERING
# -----------------------------
df["price_per_vote"] = df["price"] / (df["votes"] + 1)
df["log_votes"] = np.log1p(df["votes"])

# -----------------------------
# 4. ONE-HOT ENCODING
# -----------------------------
df = pd.get_dummies(df)

# Align columns with training data
df = df.reindex(columns=feature_columns, fill_value=0)

# -----------------------------
# 5. SCALING
# -----------------------------
df_scaled = scaler.transform(df)

# -----------------------------
# 6. PREDICTION
# -----------------------------
predicted_rating = model.predict(df_scaled)

print("\nPredicted Restaurant Rating:", round(predicted_rating[0], 2))
