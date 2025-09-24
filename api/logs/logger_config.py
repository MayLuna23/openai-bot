import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime


# Nombre del archivo con la fecha actual
log_filename = f"logs/{datetime.now().strftime('%Y-%m-%d')}.log"

# Configuración básica del logger
logger = logging.getLogger("news_api")
logger.setLevel(logging.INFO)

# Formato de logs
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Handler para consola
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Handler para archivo diario
file_handler = TimedRotatingFileHandler(
    log_filename, when="midnight", interval=1, backupCount=7, encoding="utf-8"
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
