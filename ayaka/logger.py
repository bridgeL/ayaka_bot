import sys
from loguru import logger

logger.remove()
logger.add(
    sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> \t| <blue>{name}:{function}:{line}</blue> - {message}", level="DEBUG", backtrace=False, diagnose=False)
logger.add(
    open("error.log", "a+", encoding="utf8"), format="\n\n<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> \t| <blue>{name}:{function}:{line}</blue> - {message}", level="ERROR", backtrace=False, diagnose=False)
