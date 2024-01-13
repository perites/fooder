from peewee import Model, DateField, ForeignKeyField, TextField, SqliteDatabase

import confg

db = SqliteDatabase("fooder.db")


class Ingredient(Model):
    name = TextField(unique=True)
    where_to_buy = TextField(choices=confg.places_where_to_buy)

    class Meta:
        database = db


class DishName(Model):
    name = TextField(unique=True)

    class Meta:
        database = db


class IngrToDish(Model):
    dish = ForeignKeyField(DishName, backref="ingredients")
    ingr = ForeignKeyField(Ingredient)
    ingr_amount = TextField()

    class Meta:
        database = db


class DateDish(Model):
    date = DateField()
    type = TextField(choices=(
        ("lunch", "lunch"),
        ("dinner", "dinner")
    ))
    dish = ForeignKeyField(DishName)

    class Meta:
        database = db

# db.create_tables([DishName, Ingredient, IngrToDish, DateDish])
# db.drop_tables(DateDish)
# DishName.create(name="Dish3")
# Ingredient.create(name="IngrRR1", where_to_buy='Zabka')
# Ingredient.create(name="IngrRR2", where_to_buy='Zabka')
# Ingredient.create(name="IngrRR3", where_to_buy='Zabka')

# IngrToDish.create(dish=DishName.get(DishName.name == "Dish2"),
#                   ingr=Ingredient.get(Ingredient.name == "IngrRR1"), ingr_amount="t lozek")
# IngrToDish.create(dish=DishName.get(DishName.name == "Dish2"),
#                   ingr=Ingredient.get(Ingredient.name == "IngrRR2"), ingr_amount="v lozek")
# IngrToDish.create(dish=DishName.get(DishName.name == "Dish2"),
#                   ingr=Ingredient.get(Ingredient.name == "IngrRR3"), ingr_amount="z lozek")

# DateDish.create(date=datetime.date.today() + datetime.timedelta(days=1), type="lunch",
#                 dish=DishName.get(DishName.name == "Dish1"))
# DateDish.create(date=datetime.date.today() + datetime.timedelta(days=1), type="dinner",
#                 dish=DishName.get(DishName.name == "Dish2"))
