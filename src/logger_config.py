import logging


def setup_logging():
    """Конфикурация logging"""
    logging.basicConfig(
        filename="log_file.txt",
        filemode="w",
        encoding="UTF-8",
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger()