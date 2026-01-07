import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# PROJECT ROOT (single source)
# -----------------------------
PROJECT_ROOT = Path(
    os.getenv("PROJECT_ROOT", Path(__file__).resolve().parents[1])
)

# -----------------------------
# PATH CONFIGURATION
# -----------------------------
RAW_DATA_PATH = Path(
    os.getenv("RAW_DATA_PATH", PROJECT_ROOT / "data" / "raw")
)

LOG_DIR = Path(
    os.getenv("LOG_DIR", PROJECT_ROOT / "logs")
)

# -----------------------------
# DATABASE CONFIG
# -----------------------------
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# -----------------------------
# VALIDATION
# -----------------------------
required = [DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]
if not all(required):
    raise EnvironmentError(
        "Missing required DB environment variables"
    )
