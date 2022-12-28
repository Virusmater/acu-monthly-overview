from datetime import datetime, date
from time import strptime

from dateutil import relativedelta
from flask import Flask, render_template, request, url_for, make_response
from src import parser
from src.month import Month

application = Flask(__name__)


@application.route("/")
def main():
    month = request.args.get('month')
    if not month:
        currentDateTime = datetime.now()
        date = currentDateTime.date()
        date = date + relativedelta.relativedelta(months=1)
        print(date)
        month = date.strftime("%B")
    events = parser.get_events(month)
    sneak = []
    if 0 < len(events) < 33:
        extra = 33 - len(events)
        month = next_month(events[0].year, month)
        sneak = parser.get_events(month)[:extra]
    artist = parser.get_art()
    return render_template('main.html', events=events, sneak=sneak, artist=artist, months=month_list(),
                           selected_month=month)


def next_month(year, month):
    month = strptime(month, '%B').tm_mon
    nm = date(int(year), month, 1) + relativedelta.relativedelta(days=31)
    return nm.strftime('%B')


def month_list():
    m = []
    import calendar
    for i in range(1, 13):
        month = Month()
        month.number = i
        month.name = calendar.month_name[i]
        m.append(month)  # month_name is an array
    return m
