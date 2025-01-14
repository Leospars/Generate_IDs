# lib/configured_log.py
import logging
from lib.paths import BASE_DIR

ENABLE_COLOR = False

# ANSI color codes and text formatting
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, GREY = [""] * 9
BOLD, UNDERLINE, ITALICS, RESET = [""] * 4

if ENABLE_COLOR:
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, GREY = (
        "\033[0;30m", "\033[0;31m", "\033[0;32m", "\033[0;33m", "\033[0;34m", "\033[0;35m", "\033[0;36m",
        "\033[0;37m", "\033[1;30m"
    )
    BOLD, UNDERLINE, ITALICS, RESET = "\033[1m", "\033[4m", "\033[3m", "\033[0m"

logging.basicConfig(
    level=logging.DEBUG,
    format=f'\n<%(asctime)s> {GREY}%(levelname)-9s| %(name)-10s - {CYAN}%(funcName)-10s:{RESET}\n%(message)s',
    handlers=[
        logging.FileHandler(BASE_DIR / "app.log"),
        logging.StreamHandler()
    ]
)

# Set the logging level for PIL.PngImagePlugin to WARN to ignore logs
logging.getLogger("PIL.PngImagePlugin").setLevel(logging.INFO)

log = logging.getLogger(__name__).debug
log_error = logging.error

if __name__ == "__main__":
    log("This is a test log")
    logging.error("This is a test error")