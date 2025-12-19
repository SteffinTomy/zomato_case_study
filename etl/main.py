import os
from extract import extract_all_csvs
from transform import transform, explode_cuisines
from load import load_to_staging

BASE_PATH = r"C:\ILP2025_01_SDET_WS_16082025\OJT_CASE_STUDY\zomato_case_study\data\raw"

print("BASE_PATH exists:", os.path.exists(BASE_PATH))

# --------------------
# EXTRACT
# --------------------
df = extract_all_csvs(BASE_PATH)

if df.empty:
    print("No data extracted. Exiting.")
    exit(1)

print(f"Rows extracted: {len(df)}")

# --------------------
# TRANSFORM
# --------------------
df = transform(df)
df = explode_cuisines(df)

print(f"Rows after transform: {len(df)}")

# --------------------
# LOAD
# --------------------
load_to_staging(df)

print("ETL completed successfully")
print("Total rows loaded:", len(df))
