"""Initialize logging with good defaults"""
from typing import Optional, Dict, Any, cast
import logging
import logging.config
import time
import datetime
import copy


class UTCISOFormatter(logging.Formatter):
    """Output timestamps in UTC ISO timestamps"""

    converter = time.gmtime

    def formatTime(self, record: logging.LogRecord, datefmt: Optional[str] = None) -> str:
        converted = datetime.datetime.fromtimestamp(record.created, tz=datetime.timezone.utc)
        if datefmt:
            formatted = converted.strftime(datefmt)
        else:
            formatted = converted.isoformat(timespec="milliseconds")
        return formatted.replace("+00:00", "Z")


DEFAULT_LOG_FORMAT = (
    "[%(asctime)s][%(levelname)s] %(name)s (%(process)d) %(pathname)s:%(funcName)s:%(lineno)d | %(message)s"
)
DEFAULT_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "utc": {
            "()": UTCISOFormatter,
            "format": DEFAULT_LOG_FORMAT,
        },
        "local": {
            "format": DEFAULT_LOG_FORMAT,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "utc",
        },
    },
    "root": {
        "handlers": ["console"],
    },
}


def init_logging(level: int = logging.INFO) -> None:
    """Initialize logging, call this if you don't know any better logging arrangements"""
    config = cast(Dict[str, Any], copy.deepcopy(DEFAULT_LOGGING_CONFIG))
    config["root"]["level"] = level
    logging.config.dictConfig(config)
