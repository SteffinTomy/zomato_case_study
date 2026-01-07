import logging
from logging.handlers import RotatingFileHandler
from config import LOG_DIR

def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Ensure logs directory exists
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    log_file = LOG_DIR / "etl.log"

    # Explicitly create log file if it does not exist
    if not log_file.exists():
        log_file.touch()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # File handler (rotating)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5_000_000,
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
