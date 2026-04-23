import logging
from logging import Formatter, FileHandler

def setup_logging(verbose: bool):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    try:
        from rich.logging import RichHandler

        console = RichHandler(
            rich_tracebacks=True,
            show_time=False,
            show_path=False
        )
    except ImportError:
        console = logging.StreamHandler()

    console.setLevel(logging.INFO)
    console.setFormatter(Formatter("%(message)s"))
    logger.addHandler(console)

    if verbose:
        file_handler = FileHandler("debug.log")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
            Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )
        logger.addHandler(file_handler)
