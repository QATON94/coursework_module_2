import logging
from pathlib import Path


def setup_logging():
    """Конфикурация logging"""
    ROOT_PATH = Path(__file__).parent.parent
    filename = ROOT_PATH.joinpath("data", "log_file.txt")
    logging.basicConfig(
        filename=filename,
        filemode="w",
        encoding="UTF-8",
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger()
