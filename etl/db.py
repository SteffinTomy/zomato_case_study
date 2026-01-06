from sqlalchemy import create_engine
from urllib.parse import quote_plus
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from logger import get_logger

logger = get_logger("DB")

def get_engine():
    if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
        logger.critical("Database configuration missing")
        raise EnvironmentError("Database configuration incomplete")

    encoded_password = quote_plus(DB_PASSWORD)

    connection_string = (
        f"mysql+pymysql://{DB_USER}:{encoded_password}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    try:
        engine = create_engine(
            connection_string,
            pool_pre_ping=True
        )
        logger.info("Database engine created successfully")
        return engine
    except Exception:
        logger.critical("Failed to create database engine", exc_info=True)
        raise
