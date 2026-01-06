import os
from pathlib import Path

# ---------------------------
# PROJECT ROOT
# ---------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------
# RAW DATA PATH
# ---------------------------
RAW_DATA_PATH = os.getenv(
    "RAW_DATA_PATH",
    str(PROJECT_ROOT / "data" / "raw")
)

# ---------------------------
# DATABASE CONFIG
# ---------------------------
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "zomato_analytics")
