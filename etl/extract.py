import os
import glob
import pandas as pd
from logger import get_logger
from exceptions import ExtractionError

logger = get_logger("EXTRACT")

REQUIRED_COLUMNS = {
    "name", "price", "cusine_category", "city",
    "region", "url", "page no", "cusine type",
    "timing", "rating_type", "rating", "votes"
}

def extract_all_csvs(base_path):
    if not base_path.exists():
        raise ExtractionError(f"Raw data path not found: {base_path}")

    files = glob.glob(str(base_path / "**" / "*.csv"), recursive=True)

    if not files:
        raise ExtractionError("No CSV files found in raw data path")

    logger.info(f"Found {len(files)} CSV files")

    dataframes = []

    for idx, file in enumerate(files, start=1):
        try:
            logger.info(f"Reading file {idx}: {file}")

            df = pd.read_csv(file, sep="|", engine="python")

            df.columns = [c.strip().lower() for c in df.columns]

            missing = REQUIRED_COLUMNS - set(df.columns)
            if missing:
                raise ExtractionError(
                    f"Missing columns {missing} in file {file}"
                )

            df["source_file"] = os.path.basename(file)
            df["source_city"] = os.path.basename(os.path.dirname(file))

            dataframes.append(df)

        except Exception as e:
            logger.error(f"Failed to read {file}", exc_info=True)
            continue  # skip bad file, continue ETL

    if not dataframes:
        raise ExtractionError("All CSV files failed during extraction")

    return pd.concat(dataframes, ignore_index=True)
