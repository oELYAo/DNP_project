import logging
import logging.handlers
import os

LOG_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "app.log"
)
LOG_FILE = os.path.abspath(LOG_FILE)

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(log_level=logging.INFO, log_file=LOG_FILE):
    """
    Set up logging configuration for the project.
    Logs to both console and a file with a standard format.
    """
    logger = logging.getLogger()
    logger.setLevel(log_level)

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler (rotating)
    fh = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=3
    )
    fh.setLevel(log_level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Avoid duplicate logs if setup_logging is called multiple times
    logger.propagate = False


def get_logger(name=None):
    """
    Get a logger with the given name, ensuring logging is configured.
    """
    if not logging.getLogger().handlers:
        setup_logging()
    return logging.getLogger(name)
