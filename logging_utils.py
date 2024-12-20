import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_file: str):
    """Set up logging with a rotating file handler."""
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=1)  # 10 MB per file
    handler.setFormatter(log_formatter)

    logger = logging.getLogger("transcription_logger")
    logger.setLevel(logging.INFO)  # Adjust log level if needed
    logger.addHandler(handler)

    return logger