# lib/configured_log.py
import logging

# ANSI color codes
BLACK = "\033[0;30m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
BLUE = "\033[0;34m"
MAGENTA = "\033[0;35m"
CYAN = "\033[0;36m"
WHITE = "\033[0;37m"
GREY = "\033[1;30m"

# Text formatting
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
ITALICS = "\033[3m"

# Reset color
RESET = "\033[0m"

logging.basicConfig(
    level=logging.DEBUG,
    format=f'{GREY}%(name)s|{CYAN}%(funcName)s:{RESET} %(message)s',
    handlers=[
        logging.FileHandler("../app.log"),
        logging.StreamHandler()
    ]
)

# Set the logging level for PIL.PngImagePlugin to WARN to ignore logs
logging.getLogger("PIL.PngImagePlugin").setLevel(logging.INFO)

log = logging.getLogger(__name__).debug
