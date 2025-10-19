import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name: str = None) -> logging.Logger:

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  

    if logger.handlers:
        return logger

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)

    logger.addHandler(console_handler)

    # No noise for Quart, Asyncio & Hypercorn
    logging.getLogger("quart.app").setLevel(logging.WARNING)
    logging.getLogger("quart").setLevel(logging.WARNING)
    logging.getLogger("hypercorn.error").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("quart.utils").setLevel(logging.WARNING)
    logging.getLogger("quart.serving").setLevel(logging.WARNING)

    return logger