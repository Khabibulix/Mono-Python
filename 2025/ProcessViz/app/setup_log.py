import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(name: str = None) -> logging.Logger:

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "process.log")
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=3
    )
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s: %(message)s", datefmt="%H:%M:%S"
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # No noise for Quart, Asyncio & Hypercorn
    for noisy_logger in [
        "quart.app",
        "quart",
        "hypercorn.error",
        "asyncio",
        "quart.utils",
        "quart.serving",
    ]:
        logging.getLogger(noisy_logger).setLevel(logging.WARNING)

    return logger
