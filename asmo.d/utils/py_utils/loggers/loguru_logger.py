import sys

from loguru import logger
from pydantic_settings import BaseSettings


class LoggingSettings(BaseSettings):
    level: str = "WARNING"

    class Config:
        env_prefix = "LOGGING_"


logging_settings = LoggingSettings()

# Remove default logger
logger.remove()

# Log format for console and files
log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level> | "
    "{extra}"
)

# Add colorized output to console
logger.add(
    sys.stdout,
    format=log_format,
    level=logging_settings.level,
    colorize=True,
    backtrace=True,
    diagnose=True,
)

# commented due to missing permissions to create a dir and write log to files
# Create logs directory if it doesn't exist
# LOG_DIR = Path("logs")
# LOG_DIR.mkdir(exist_ok=True)
#
# # Add JSON formatted logs to file with rotation
# logger.add(
#     LOG_DIR / "app.json",
#     format=lambda record: json.dumps(
#         {
#             "timestamp": record["time"].isoformat(),
#             "level": record["level"].name,
#             "message": record["message"],
#             "name": record["name"],
#             "line": record["line"],
#             "extra": record["extra"],
#         }
#     ),
#     level="INFO",
#     rotation="10 MB",
#     retention="1 week",
#     compression="zip",
# )
#
# # Add error logs to separate file
# logger.add(
#     LOG_DIR / "error.log",
#     format=log_format,
#     level="ERROR",
#     rotation="10 MB",
#     retention="1 week",
#     backtrace=True,
#     diagnose=True,
# )


def get_logger(name: str) -> logger:
    return logger.bind(name=name)
