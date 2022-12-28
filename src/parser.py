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

def get_events(target_month):
    url_agenda = "https://acu.nl/agenda/"
    req_agenda = requests.get(url_agenda, headers)
    soup_agenda = BeautifulSoup(req_agenda.content, 'html.parser')
    soup_agenda = soup_agenda.find("div", id="AgendaWrap")
    agenda_elements = soup_agenda.find_all("li", class_="AgendaEntry")
    events = []
    for event_li in agenda_elements:
        is_cancelled = event_li.find("div", class_="CancelledEvent")
        if is_cancelled:
            continue
        month = event_li.find("span", class_="AgendaMonth").get_text()
        if target_month != month:
            continue
        event = Event()
        event.year = event_li.find("span", class_="AgendaYear").get_text()
        event.month = month
        event.title = event_li.find("div", class_="AgendaTitle").find("h2").get_text()
        event.subtitle = event_li.find("div", class_="AgendaTitle").find("h3").get_text()
        date = event_li.find("span", class_="AgendaDay").get_text()
        if len(date) == 3:
            date = "0" + date
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


def get_art():
    url_art = "https://acu.nl/"
    req_art = requests.get(url_art, headers)
    soup_art = BeautifulSoup(req_art.content, 'html.parser')
    soup_art = soup_art.find("h4", class_="HomeArtArtist")
    return soup_art.getText()
