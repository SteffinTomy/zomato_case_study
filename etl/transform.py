import pandas as pd
from logger import get_logger
from exceptions import TransformationError

logger = get_logger("TRANSFORM")

def transform(df):
    try:
        df.columns = [c.lower().strip().replace(" ", "_") for c in df.columns]

        df = df.rename(columns={
            "name": "restaurant_name",
            "cusine_category": "cuisine_category",
            "cusine_type": "cuisine_type"
        })

        for col in ["price", "rating", "votes"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df["price"].fillna(0, inplace=True)
        df["votes"].fillna(0, inplace=True)

        before = len(df)
        df = df.dropna(subset=["restaurant_name", "rating"])
        dropped = before - len(df)

        if dropped:
            logger.warning(f"Dropped {dropped} rows due to missing mandatory fields")

        return df

    except Exception as e:
        logger.critical("Transformation failed", exc_info=True)
        raise TransformationError from e


def explode_cuisines(df):
    try:
        df["cuisine_category"] = df["cuisine_category"].str.split(",")
        df = df.explode("cuisine_category")
        df["cuisine_category"] = df["cuisine_category"].str.strip()
        return df

    except Exception as e:
        logger.critical("Cuisine explosion failed", exc_info=True)
        raise TransformationError from e
