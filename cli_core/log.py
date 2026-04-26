import logging
import logging.config
from logging import Formatter, FileHandler
from pathlib import Path
from cli_core.files import new_file_path

def build_logging_config(verbose: bool = False, output: Path | str = None):
    handlers = {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
        }
    }

    formatters = {
        "simple": {
            "format": "%(message)s"
        },
        "detailed": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        }
    }

    try:
        import rich.logging

        handlers["console"] = {
            "class": "rich.logging.RichHandler",
            "level": "INFO",
            "formatter": "simple",
            "rich_tracebacks": True,
            "show_time": False,
            "show_path": False,
        }
    except ImportError:
        pass

    root_handlers = ["console"]

    if verbose:
        logfile = str(new_file_path(output, "debug.log"))

        handlers["file"] = {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": logfile,
        }

        root_handlers.append("file")

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": formatters,
        "handlers": handlers,
        "root": {
            "level": "DEBUG",
            "handlers": root_handlers,
        },
    }

def setup_logging(
    verbose: bool = False,
    output_fullpath: Path | str = None,
    logging_config: dict | None = None
):
    if isinstance(logging_config, dict):
        if not logging_config:
            raise ValueError("logging_config cannot be empty")
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
