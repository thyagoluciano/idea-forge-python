# src/core/utils/logger.py
import logging


def setup_logger(name, level=logging.INFO):
    """Sets and returns a logger."""
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger