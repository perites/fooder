import logging

from functools import wraps


def error_catcher(func):
    @wraps(func)
    def wrapper(*args, **kwds):
        try:
            return func(*args, **kwds)

        except Exception as e:
            error_code = e.code if hasattr(e, "code") else 500
            logging.error(f"Error occured : {e.__str__()} ; code : {error_code}")
            return {"message": e.__str__()}, error_code

    return wrapper
