import time
from pathlib import Path

def new_file_path(fullpath=None, fallback="output"):
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    p = Path(fullpath if fullpath else fallback)
    return Path(f"{p.stem}-{timestamp}{p.suffix}")
