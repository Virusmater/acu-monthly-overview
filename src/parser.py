import requests as requests
from bs4 import BeautifulSoup

from src.event import Event

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

url = "https://acu.nl/agenda/"
req = requests.get(url, headers)
soup = BeautifulSoup(req.content, 'html.parser')
soup = soup.find("div", id="AgendaWrap")
agenda_elements = soup.find_all("li", class_="AgendaEntry")


def get_events(target_month):
    events=[]
    for event_li in agenda_elements:
        month = event_li.find("span", class_="AgendaMonth").get_text()
        if target_month != month:
            continue
        event = Event()
        event.month = month
        event.title = event_li.find("div", class_="AgendaTitle").find("h2").get_text()
        event.subtitle = event_li.find("div", class_="AgendaTitle").find("h3").get_text()
        date = event_li.find("span", class_="AgendaDay").get_text()
        if len(date) == 3:
            date = "0"+date
        date = date[0:2]
        event.date = date
        if events and date == events[-1].date:
            event.same_day = True
        event.weekday = event_li.find("span", class_="AgendaWeekday").get_text()
        agenda_details = event_li.find_all("span", class_="AgendaDetail")
        if len(agenda_details) == 3:
            event.time = agenda_details[1].get_text()
            event.set_price(agenda_details[2].get_text())
        else:
            event.time = event_li.find_all("span", class_="AgendaDetail")[0].get_text()
            event.set_price(agenda_details[1].get_text())
        events.append(event)
    return events
