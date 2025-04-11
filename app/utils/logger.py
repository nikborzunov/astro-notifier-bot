# utils/logger.py

import logging
import colorlog

logger = logging.getLogger("astro_notifier")
logger.setLevel(logging.DEBUG)

handler = colorlog.StreamHandler()
handler.setLevel(logging.DEBUG)

formatter = colorlog.ColoredFormatter(
    fmt="%(log_color)s%(asctime)s [%(levelname)s] 🚀 %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'bold_red',
    }
)

handler.setFormatter(formatter)
logger.handlers.clear()
logger.addHandler(handler)
