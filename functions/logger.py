import logging
import os


_LOG_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "log.txt",
)
_IS_CONFIGURED = False


def _configure_logging() -> None:
    global _IS_CONFIGURED

    if _IS_CONFIGURED:
        return

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(_LOG_FILE_PATH, mode="a", encoding="utf-8")
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    _IS_CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    _configure_logging()
    return logging.getLogger(name)