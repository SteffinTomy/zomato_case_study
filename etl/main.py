import sys
from pathlib import Path
from extract import extract_all_csvs
from transform import transform, explode_cuisines
from load import load_to_staging
from config import RAW_DATA_PATH
from logger import get_logger

logger = get_logger("MAIN")

def main():
    raw_path = Path(RAW_DATA_PATH)

    logger.info(f"Raw data path: {raw_path}")

    if not raw_path.exists():
        logger.critical(f"Raw data path does not exist: {raw_path}")
        sys.exit(1)

    # --------------------
    # EXTRACT
    # --------------------
    try:
        df = extract_all_csvs(raw_path)
        logger.info(f"Rows extracted: {len(df)}")
    except Exception:
        logger.critical("Extraction failed", exc_info=True)
        sys.exit(1)

    if df.empty:
        logger.warning("No data extracted. Exiting ETL.")
        sys.exit(0)

    # --------------------
    # TRANSFORM
    # --------------------
    try:
        df = transform(df)
        df = explode_cuisines(df)
        logger.info(f"Rows after transform: {len(df)}")
    except Exception:
        logger.critical("Transformation failed", exc_info=True)
        sys.exit(1)

    # --------------------
    # LOAD
    # --------------------
    try:
        load_to_staging(df)
        logger.info(f"Total rows loaded: {len(df)}")
    except Exception:
        logger.critical("Load failed", exc_info=True)
        sys.exit(1)

    logger.info("ETL completed successfully")

if __name__ == "__main__":
    main()
