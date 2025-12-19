from db import get_engine

def load_to_staging(df):
    engine = get_engine()

    df.rename(columns={
        "restaurant_name": "name"
    }, inplace=True)

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
