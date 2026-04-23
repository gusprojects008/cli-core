import logging
import logging.config
from logging import Formatter, FileHandler
from cli_util.files import new_file_path

def setup_logging(
    verbose: bool = False,
    output_fullpath: str = None,
    logging_config: dict | None = None
):
    if logging_config is not None:
        logging.config.dictConfig(logging_config)
        return

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
        file_handler = FileHandler(str(new_file_path(output_fullpath, "debug.log")))
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
            Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )
        logger.addHandler(file_handler)
