from logging import getLogger
from logging.config import dictConfig
from .config import LOGGER_CONFIG_JSON

dictConfig(LOGGER_CONFIG_JSON)
logger = getLogger('bot')
