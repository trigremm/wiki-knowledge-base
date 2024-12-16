import logging
import sys

from pydantic_settings import BaseSettings


class LoggingSettings(BaseSettings):
    level: str = "WARNING"

    class Config:
        env_prefix = "LOGGING_"


logging_settings = LoggingSettings()


def get_logger(name: str = __name__, level: str = None) -> logging.Logger:
    """Get a logger instance"""

    logger = logging.getLogger(name)

    if not logger.handlers:
        # Set log level, using local level if provided, otherwise global
        logger_level = level or getattr(logging, logging_settings.level)
        logger.setLevel(logger_level)

        # Create a formatter
        formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

        # Create a console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
