import sys

from loguru import logger

FORMAT: str = "{time:DD-MMM-YYYY HH:mm:ss} | {level} | {message}"


logger.remove()
logger.add(sys.stderr, format=FORMAT)
