import logging
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

        self.weekday = self.date.isocalendar()[2]

    def update_menu(self, action: str, dish_name: str):
        dish = DishName.get(DishName.name == dish_name)

        match action:
            case "dish_lunch":
                logging.info(f"add dish {dish} to lunch to day at date {self.date}")

                DateDish.create(date=self.date, type="lunch", dish=dish)
            case "dish_dinner":
                logging.info(f"add dish {dish} to dinner to day at date {self.date}")

                DateDish.create(date=self.date, type="dinner", dish=dish)
            case "dish_lunch_delete":
                logging.info(f"delete dish {dish} from lunch to day at date {self.date}")

                qry = DateDish.delete().where(
                    (DateDish.date == self.date) & (DateDish.type == "lunch") & (DateDish.dish == dish))
                qry.execute()

            case "dish_dinner_delete":
                logging.info(f"delete dish {dish} from dinner to day at date {self.date}")

                qry = DateDish.delete().where(
                    (DateDish.date == self.date) & (DateDish.type == "dinner") & (DateDish.dish == dish))
                qry.execute()

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
        self.name = self.dish_name_obj.name
        self.ingredients_objs = self.dish_name_obj.ingredients

    def update(self, form):
        action = form["action"]
        match action:
            case "delete_dish":
                qry = IngrToDish.delete().where(IngrToDish.dish == self.dish_name_obj)
                qry.execute()
                qry = DateDish.delete().where(DateDish.dish == self.dish_name_obj)
                qry.execute()
                qry = DishName.delete().where(DishName.name == self.name)
                qry.execute()

                logging.info(f"delete dish named {self.name}")

            case "change_name":
                self.dish_name_obj.name = form['new_name']
                try:
                    self.dish_name_obj.save()
                except Exception as e:
                    pass

                logging.info(f'change name for dish {self.name} to {form["new_name"]}')
                self.name = self.dish_name_obj.name

            case "delete_ingr":
                qry = IngrToDish.delete().where((IngrToDish.dish == self.dish_name_obj) & (
                        IngrToDish.ingr == Ingredient.get(Ingredient.name == form["ingr_to_delete"])))
                qry.execute()
                logging.info(f"delete ingr named {form['ingr_to_delete']} from dish {self.name}")

            case "change_ingr_amount":
                pare = list(IngrToDish.select().where((IngrToDish.dish == self.dish_name_obj) & (
                        IngrToDish.ingr == Ingredient.get(Ingredient.name == form["ingr_to_change"]))))[0]
                pare.ingr_amount = form["new_amount"]
                pare.save()
                logging.info(
                    f'change amount of ingr {form["ingr_to_change"]} to {form["new_amount"]} in dish {self.name}')

            case "add_ingr":
                IngrToDish.create(dish=self.dish_name_obj, ingr=Ingredient.get(Ingredient.name == form["ingr_to_add"]),
                                  ingr_amount=form["amount"])
                logging.info(f'add ingr {form["ingr_to_add"]} with amount {form["amount"]} to dish {self.name}')


def change_ingr(form: dict):
    ingr_name = form.get('ingr_name')
    ingr_place = form.get('where_to_buy')
    action = form['action']

    if action == "add_new_ingr":
        Ingredient.create(name=ingr_name, where_to_buy=ingr_place)
        logging.info(f"add new ingr with name : {ingr_name} place : {ingr_place}")
        return

    ingr = Ingredient.get(Ingredient.name == ingr_name)

    match action:
        case "change_name":
            new_name = form['new_name']

            ingr.name = new_name
            ingr.save()
            logging.info(f"change name ingr {ingr_name} to {new_name}")

        case "change_place":
            ingr.where_to_buy = ingr_place
            ingr.save()
            logging.info(f"change place for ingredient {ingr_name} to place {ingr_place}")

        case "delete":
            qry = IngrToDish.delete().where(IngrToDish.ingr == ingr)
            qry.execute()

            ingr.delete_instance()
            logging.info(f"delete ingr with name {ingr_name}")

    return
