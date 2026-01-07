from extract import extract_all_csvs
from transform import transform, explode_cuisines
from load import load_to_staging
from config import RAW_DATA_PATH
from logger import get_logger
from exceptions import ETLError

logger = get_logger("MAIN")

def main():
    try:
        df = extract_all_csvs(RAW_DATA_PATH)
        logger.info(f"Rows extracted: {len(df)}")

        df = transform(df)
        df = explode_cuisines(df)
        logger.info(f"Rows after transform: {len(df)}")

        load_to_staging(df)
        logger.info("ETL completed successfully")

    except ETLError:
        logger.critical("ETL pipeline failed", exc_info=True)
        raise
    except Exception:
        logger.critical("Unexpected fatal error", exc_info=True)
        raise

if __name__ == "__main__":
    main()
