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
        month = date.strftime("%B")
    events = parser.get_events(month)

    artist = parser.get_art()
    recurrent = process_recurrent(events)
    sneak = []
    total = len(events) + len(recurrent)
    if 0 < total < 25:
        extra = 25 - total
        month = next_month(events[0].year, month)
        sneak = parser.get_events(month)
        # remove weekly events for sneak peek
        sneak = [event for event in sneak if event.is_weekly is False]
        same_day(sneak)
        sneak = sneak[:extra]
    same_day(events)
    return render_template('main.html', events=events, sneak=sneak, recurrent=recurrent, artist=artist,
                           months=month_list(),
                           selected_month=month)


def same_day(events):
    date = ""
    for event in events:
        if date == event.date:
            event.same_day = True
        date = event.date


def process_recurrent(events, limit=2):
    recurrent = []
    original_list = list(events)
    for event in list(original_list):
        if sum(1 for i in original_list if (i.title == event.title) and (i.weekday == event.weekday)) > limit:
            event.recurrent = True
            events.remove(event)
            if sum(1 for i in recurrent if (i.title == event.title) and (i.weekday == event.weekday)) == 0:
                if recurrent and event.date == recurrent[-1].date:
                    event.same_day = True
                recurrent.append(event)
    recurrent = sorted(recurrent,
                       key=lambda x: x.weekday_num
                       )
    return recurrent


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
