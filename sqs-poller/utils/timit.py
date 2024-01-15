import time
from loguru import logger


def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.critical(f"{func.__name__} took {end_time - start_time} seconds")
        return result

    return wrapper
