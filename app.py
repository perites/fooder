import datetime
import logging

from flask import Flask, redirect, render_template, request
from flask_login import login_required, UserMixin, LoginManager, login_user

from tools import Day, Week, Dish, DishName
from decorators import error_catcher
import confg

app = Flask(__name__)
app.config["SECRET_KEY"] = 'c42e8d7afdsdfds56342385cb9e30b6b'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


logging.basicConfig(format='%(levelname)s: %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    filename='fooder.log', filemode='w', level=logging.DEBUG)


@app.route('/login', methods=["GET"])
@error_catcher
def login():
    next_url = request.args.get('next')
    return render_template("login.html", next_url=next_url)


@app.route('/login', methods=["POST"])
@error_catcher
def login_post():
    next_url = request.args.get('next')

    form = request.form.to_dict()
    username = form['username']
    password = form['password']
    if username == confg.username and password == confg.password:
        login_user(User(username))
        return redirect(next_url) if next_url else redirect("/")

    return redirect(f"/login?next={next_url}")


@app.route('/')
@error_catcher
def home():
    today_date = datetime.date.today()
    return redirect(f"/day/{today_date}")


@app.route("/day/<date>/")
@error_catcher
def dishes_for_date(date):
    date = datetime.datetime.strptime(date, confg.date_format).date()
    day = Day(date)
    return render_template("day.html", day=day)


@app.route("/list/<date>/")
@error_catcher
def list_for_date(date):
    date = datetime.datetime.strptime(date, confg.date_format).date()
    day = Day(date)

    return day.ingredients_list()


@app.route('/week/<date>/')
@error_catcher
def week_menu(date):
    date = datetime.datetime.strptime(date, confg.date_format).date()
    week = Week(date)
    return render_template("week.html", week=week)


@app.route("/week/<date>/edit/", methods=["GET"])
@error_catcher
@login_required
def menu_edit_get(date):
    week = Week(datetime.datetime.strptime(date, confg.date_format).date())
    return render_template("menu_edit.html", week=week, dishes=DishName.select())


@app.route("/week/<date>/edit/", methods=["POST"])
@error_catcher
@login_required
def menu_edit_post(date):
    day = Day(datetime.datetime.strptime(date, confg.date_format).date())

    form = request.form.to_dict()
    if not form:
        return redirect(f"/week/{date}/edit")

    action = list(form.keys())[0]
    day.update_menu(action, form[action])

    return redirect(f"/week/{date}/edit")


if __name__ == '__main__':
    app.run()
