# src/core/utils/logger.py
import logging

_shared_handler = None


def setup_logger(name, level=logging.INFO):
    """Sets and returns a logger."""
    global _shared_handler

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    if not _shared_handler:
        _shared_handler = logging.StreamHandler()
        _shared_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.hasHandlers():
        logger.addHandler(_shared_handler)
    return logger
