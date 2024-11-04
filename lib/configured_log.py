# lib/configured_log.py
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s|%(funcName)s: %(message)s',
    handlers=[
        logging.FileHandler("../app.log"),
        logging.StreamHandler()
    ]
)

log = logging.getLogger(__name__).debug
