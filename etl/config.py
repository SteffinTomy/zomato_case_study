import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database credentials
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Raw data path (relative + overrideable)
RAW_DATA_PATH = Path(
    os.getenv("RAW_DATA_PATH", BASE_DIR / "data" / "raw")
)

# Validate required environment variables
REQUIRED_VARS = [
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
]

if not all(REQUIRED_VARS):
    raise EnvironmentError(
        "Missing one or more required environment variables. "
        "Check your .env file."
    )
