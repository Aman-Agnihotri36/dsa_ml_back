# exception_handler.py
from functools import wraps
from src.utils.customLogger import logger

def handle_exceptions(func):
    """
    Decorator to wrap functions with centralized exception handling.
    Any exception is logged using the global logger.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Exception in function '{func.__name__}': {e}", exc_info=True)
            # Optionally, re-raise if you want the exception to propagate
            # raise e
    return wrapper
