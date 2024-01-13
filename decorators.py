import logging

from functools import wraps

from flask import redirect
from tools import Dish, DishName


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


def if_exists_dish(func):
    @wraps(func)
    def wrapper(*args, **kwds):
        try:
            dish = Dish(DishName.get(DishName.name == kwds["dish_name"]))
            return func(dish)

        except Exception:
            return redirect("/")

    return wrapper
