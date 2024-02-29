import logging
from instance.config import LOG_LEVEL

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("./logs/interview_app.error.log")
formatter = logging.Formatter(
    "[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %z",
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(LOG_LEVEL)
