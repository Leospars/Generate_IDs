import os
from pathlib import Path
from lib.configured_log import log

log(f"Paths: {Path(__file__).resolve()}")
def eval_base_dir(base_dir: Path) -> Path:
    if (base_dir / "_internal").exists() and (base_dir / "_internal").is_dir() :
        if base_dir.parent.parent  == "dist":
            base_dir = base_dir / "_internal"
            # This is a compiled distribution
            log(f"Exe file: {Path(__file__)}")
    else:
        log(f"Running from python file: {__name__}")
    return base_dir

# ../.. => ./lib/paths or ./dist/_internal/lib/paths or ./dist/lib/paths
BASE_DIR = eval_base_dir(Path(__file__).resolve().parent.parent)
log(f"Base Dir: {BASE_DIR}")

FONT_DIR = BASE_DIR / "font"
IMG_DIR = BASE_DIR / "img"
def get_downloads_directory():
    if os.name == "nt":
        return os.path.join(os.environ['USERPROFILE'], 'Downloads')
    elif os.name == "posix":
        return os.path.join(os.environ['HOME'], 'Downloads')
    else:
        return None