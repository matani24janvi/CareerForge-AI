from os import makedirs as makeDirectory
from os.path import join as pathJoin

from logging import Formatter, Logger, getLogger, ERROR, INFO, WARNING
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
makeDirectory(LOG_DIR, exist_ok=True)

def create_logger(name: str, filename: str, level=INFO) -> Logger:
    logger = getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        log_path = pathJoin(LOG_DIR, filename)
        handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=5)
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

error_logger = create_logger('error', 'error.log', ERROR)
event_logger = create_logger('event', 'event.log', INFO)
db_logger = create_logger('db', 'db.log', WARNING)
access_logger = create_logger('access', 'access.log', INFO)
email_logger = create_logger('email', 'email.log', INFO)