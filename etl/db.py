from sqlalchemy import create_engine
from urllib.parse import quote_plus
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

def get_engine():
    encoded_password = quote_plus(DB_PASSWORD)

    connection_string = (
        f"mysql+pymysql://{DB_USER}:{encoded_password}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    print("CONNECTION STRING USED:")
    print(connection_string)

    engine = create_engine(
        connection_string,
        pool_pre_ping=True
    )
    return engine
