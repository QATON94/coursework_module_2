from src.logger_config import setup_logging

logger = setup_logging()


def test_function():
    logger.info('a message')
    logger.error('an error')
