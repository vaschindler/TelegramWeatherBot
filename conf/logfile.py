import logging
import functools


def log():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    return logger


def logging_decorator(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = log()
        try:
            return func(*args, **kwargs)
        except:
            err = "There was an exception in "
            err += func.__name__
            logger.exception(err)
            raise

    return wrapper
