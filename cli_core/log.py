import logging
from logging import FileHandler, Formatter
from rich.logging import RichHandler

def setup_logging(verbose: bool):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    console = RichHandler(
        rich_tracebacks=True,
        show_time=False,
        show_path=False
    )

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
