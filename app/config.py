import logging
import sys
from types import FrameType
from typing import List, cast

from loguru import logger
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings

class LoggingSettings(BaseSettings):
    LOGGING_LEVEL: int = logging.INFO  # logging levels are type int

class Settings:
    API_V1_STR: str = "/api/v1"
    logging: LoggingSettings = LoggingSettings()
    PROJECT_NAME: str = "Agentic API"

    # config for pydantic settings
    class Config:
        case_sensitive = True

# loging setup
# See: https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging  # noqa

# this class intercepts python standard logging and redirects it to loguru
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        # this is the part where the log is actually logged through loguru
        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )

def setup_app_logging(config: Settings) -> None:
    """Prepare custom logging for our application."""
    LOGGERS = ("uvicorn.asgi", "uvicorn.access")
    logging.getLogger().handlers = [InterceptHandler()]
    for logger_name in LOGGERS:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler(level=config.logging.LOGGING_LEVEL)]

    logger.configure(
        handlers=[{"sink": sys.stderr, "level": config.logging.LOGGING_LEVEL}]
    )

#this creates a single instance of Settings at load time, this way when other modules
#import the class Settigs from this file, what is loaded is a single shared object
# this line is executed only once, at the start and then the settings are reused for the whole API instnce
settings = Settings()
