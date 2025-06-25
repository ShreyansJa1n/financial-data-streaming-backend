import logging
from loguru import logger
import sys
from .config import settings

class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())

logger.remove()

# Ensure root logger is set to INFO and propagate to loguru
if settings.DEBUG:
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.DEBUG, force=True)
    logger.level("DEBUG", color="<blue>")
    logger.add(sys.stdout, level="DEBUG", serialize=False, backtrace=True, diagnose=True)
else:
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO, force=True)
    logger.level("INFO", color="<green>")
    logger.add(sys.stdout, level="INFO", serialize=False, backtrace=True, diagnose=True)