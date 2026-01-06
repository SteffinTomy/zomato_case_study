from db import get_engine
from logger import get_logger
from exceptions import LoadError

logger = get_logger("LOAD")

REQUIRED_COLUMNS = {
    "restaurant_name",
    "price",
    "cuisine_category",
    "city",
    "region",
    "url",
    "page_no",
    "cuisine_type",
    "timing",
    "rating_type",
    "rating",
    "votes"
}

def load_to_staging(df):
    try:
        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise LoadError(f"Missing columns for DB load: {missing}")

        engine = get_engine()

        # Map business column → DB column
        df = df.rename(columns={
            "restaurant_name": "name"
        })

        df[[
            "name",
            "price",
            "cuisine_category",
            "city",
            "region",
            "url",
            "page_no",
            "cuisine_type",
            "timing",
            "rating_type",
            "rating",
            "votes"
        ]].to_sql(
            "staging_restaurants_raw",
            engine,
            if_exists="append",
            index=False,
            method="multi"
        )

        logger.info(f"Loaded {len(df)} rows into staging table")

    except Exception as e:
        logger.critical("Database load failed", exc_info=True)
        raise LoadError from e
