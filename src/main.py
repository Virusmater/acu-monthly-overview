from datetime import datetime
from dateutil import relativedelta
from flask import Flask, render_template, request, url_for, make_response
from src import parser
from src.month import Month

application = Flask(__name__)


@application.route("/")
def main():
    month = request.args.get('month')
    currentDateTime = datetime.now()
    date = currentDateTime.date()
    if not month:
        nextmonth = date + relativedelta.relativedelta(months=1)
        print(nextmonth)
        month = nextmonth.strftime("%B")
    events = parser.get_events(month)
    artist = parser.get_art()
    return render_template('main.html', events=events, artist=artist, months=month_list(), selected_month=month)


def month_list():
    m = []
    import calendar
    for i in range(1, 13):
        month = Month()
        month.number = i
        month.name = calendar.month_name[i]
        m.append(month)  # month_name is an array
    return m
