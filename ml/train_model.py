import pandas as pd
import os
import numpy as np
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from urllib.parse import quote_plus
import joblib

# -----------------------------
# 1. DATABASE CONFIG
# -----------------------------
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

encoded_password = quote_plus(DB_PASSWORD)

print("DB CONFIG:")
print(DB_USER, DB_HOST, DB_PORT, DB_NAME)

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# -----------------------------
# 2. LOAD DATA
# -----------------------------
query = """
SELECT
    price,
    votes,
    city,
    region,
    cuisine,
    cuisine_type,
    rating
FROM reporting_restaurants_clean
WHERE rating IS NOT NULL
"""

df = pd.read_sql(query, engine)
print("Rows loaded:", len(df))

# -----------------------------
# 3. DATA CLEANING
# -----------------------------
df["price"] = df["price"].fillna(df["price"].median())
df["votes"] = df["votes"].fillna(0)

df["city"] = df["city"].fillna("Unknown")
df["region"] = df["region"].fillna("Unknown")
df["cuisine"] = df["cuisine"].fillna("Unknown")
df["cuisine_type"] = df["cuisine_type"].fillna("Unknown")

# -----------------------------
# 4. FEATURE ENGINEERING
# -----------------------------
df["price_per_vote"] = df["price"] / (df["votes"] + 1)
df["log_votes"] = np.log1p(df["votes"])

# -----------------------------
# 5. TARGET & FEATURES
# -----------------------------
X = df.drop(columns=["rating"])
y = df["rating"]

X = pd.get_dummies(X, drop_first=True)

# -----------------------------
# 6. SCALING
# -----------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -----------------------------
# 7. TRAIN-TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# -----------------------------
# 8. MODEL TRAINING
# -----------------------------
print("Training Linear Regression...")
lr = LinearRegression()
lr.fit(X_train, y_train)
print("Linear Regression completed.")

print("Training Random Forest...")
rf = RandomForestRegressor(
    n_estimators=50, 
    max_depth=10,
    n_jobs=-1,
    random_state=42
)
rf.fit(X_train, y_train)
print("Random Forest training completed.")

# -----------------------------
# 9. EVALUATION
# -----------------------------
def evaluate(name, y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)

    print(f"\n{name}")
    print("MAE :", mae)
    print("RMSE:", rmse)
    print("R2  :", r2)


evaluate("Linear Regression", y_test, lr.predict(X_test))
evaluate("Random Forest", y_test, rf.predict(X_test))

# -----------------------------
# 10. SAVE MODEL & ARTIFACTS
# -----------------------------
os.makedirs("ml", exist_ok=True)

joblib.dump(rf, "ml/rating_model.pkl")
joblib.dump(scaler, "ml/scaler.pkl")
joblib.dump(X.columns, "ml/feature_columns.pkl")

print("\nModel training completed and saved successfully.")
