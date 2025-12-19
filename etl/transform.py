import pandas as pd

def transform(df):
    df.columns = [c.lower().strip().replace(" ", "_") for c in df.columns]

    df = df.rename(columns={
        "name": "restaurant_name",
        "cusine_category": "cuisine_category",
        "cusine_type": "cuisine_type"
    })

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["votes"] = pd.to_numeric(df["votes"], errors="coerce")

    df["price"].fillna(0, inplace=True)
    df["votes"].fillna(0, inplace=True)

    df.dropna(subset=["restaurant_name", "rating"], inplace=True)

    return df


def explode_cuisines(df):
    df["cuisine_category"] = df["cuisine_category"].str.split(",")
    df = df.explode("cuisine_category")
    df["cuisine_category"] = df["cuisine_category"].str.strip()
    return df
