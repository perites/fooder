import datetime
import logging

from flask import Flask, redirect, render_template

from tools import Day, Week
from decorators import error_catcher
import confg

app = Flask(__name__)

logging.basicConfig(format='%(levelname)s: %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    filename='fooder.log', filemode='w', level=logging.DEBUG)


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
