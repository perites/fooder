import datetime
from collections import Counter

from database import DateDish, Ingredient, DishName, IngrToDish


class Day:
    def __init__(self, date):
        self.date = date
        self.menu_for_lunch = [Dish(pare.dish) for pare in
                               list(DateDish.select().where((DateDish.date == self.date) & (DateDish.type == "lunch")))]
        self.menu_for_dinner = [Dish(pare.dish) for pare in
                                list(
                                    DateDish.select().where(
                                        (DateDish.date == self.date) & (DateDish.type == "dinner")))]

    def ingredients_list(self):
        ingredient_list = []
        _ingredient_list = []
        for dish in self.menu_for_lunch + self.menu_for_dinner:
            for pare in dish.ingredients_objs:
                _ingredient_list.append((pare.ingr.name, pare.ingr_amount))

        element_counts = Counter(_ingredient_list)

        for element, count in element_counts.items():
            ingredient_list.append(f"{element[0]} -- {element[1]} -- *{count}")

        return ingredient_list


class Week:
    def __init__(self, date):
        self.date = date
        self.week = self.make_week()

    def make_week(self):
        week = []
        week_number = self.date.isocalendar()[1]

        for n in range(-7, 8):
            new_date = self.date + datetime.timedelta(days=n)
            if new_date.isocalendar()[1] == week_number:
                week.append(new_date)

        week.sort()
        return [Day(date) for date in week]


class Dish:
    def __init__(self, dish_name_obj: DishName):
        self.dish_name_obj = dish_name_obj
        self.ingredients_objs = self.dish_name_obj.ingredients

# dish1 = Dish("Dish1")
# print(dish1.dish_name_obj.name)
# for ing in dish1.ingredients_objs:
#     print(ing.ingr.name)
#     print(ing.ingr_amount)

# day1 = Day(datetime.date.today())
# print("Lunch : ")
# for dish in day1.menu_for_lunch:
#     print(dish.dish_name_obj.name)
#     for pare in dish.ingredients_objs:
#         print(pare.ingr.name, "---", pare.ingr_amount)
#
# print("Dinner : ")
# for dish in day1.menu_for_dinner:
#     print(dish.dish_name_obj.name)
#     for pare in dish.ingredients_objs:
#         print(pare.ingr.name, "---", pare.ingr_amount)
