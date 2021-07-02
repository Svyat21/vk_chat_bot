import re
import datetime
from utilities import date_str, cities_str

re_name = re.compile(r'^[\w\-\s]{3,30}$')
re_email = re.compile(r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b')
re_date = re.compile(r'\b\d{2}-\d{2}-\d{4}\b')
re_value = re.compile(r'\b[1-5]\b')
re_phone = re.compile(r'\b\d{10}\b')


def handler_city_departure(text, state):
    state.context['choice'] = None
    match = re.match(re_name, text)
    if match:
        if state.dispatcher.checking_city_of_departure(text.title()):
            state.context['name_city_departure'] = text.title()
            return True
        else:
            state.context['available_cities'] = cities_str(state.dispatcher.departure_cities)
            return False
    else:
        return False


def handler_destination_city(text, state):
    match = re.match(re_name, text)
    if match:
        if state.dispatcher.checking_destination_city(text.title()):
            state.context['name_destination_city'] = text.title()
            return True
        else:
            state.context['available_cities'] = cities_str(state.dispatcher.destination_name_cities)
            return False
    else:
        return False


def handler_date(text, state):
    matches = re.findall(re_date, text)
    if len(matches) > 0:
        departure_day = datetime.datetime.strptime(matches[0], '%d-%m-%Y')
        now_day = datetime.datetime.now()
        if departure_day > now_day:
            state.dispatcher.selection_nearest_flights(date=departure_day)
            state.context['date'] = matches[0]
            destination_city = state.dispatcher.name_destination_city
            state.context['time'] = state.dispatcher.destination_cities[destination_city]['Время вылета']
            state.context['value_date'] = date_str(state.dispatcher.current_departure_dates)
            return True
        else:
            return False
    else:
        return False


def handler_value(text, state):
    matches = re.findall(re_value, text)
    if len(matches) > 0:
        date = state.dispatcher.current_departure_dates[int(matches[0]) - 1]
        state.context['selected_date'] = date.strftime("%d.%m.%Y")
        return True
    else:
        return False


def handler_number_seats(text, state):
    matches = re.findall(re_value, text)
    if len(matches) > 0:
        state.context['number_seats'] = matches[0]
        return True
    else:
        return False


def handler_comment(text, state):
    state.context['comment'] = text
    return True


def handler_choice(text, state):
    if text.lower() == 'да':
        state.context['choice'] = 'yes'
        return True
    elif text.lower() == 'нет':
        state.context['choice'] = 'no'
        return True
    else:
        return False


def handler_phone(text, state):
    matches = re.findall(re_phone, text)
    if len(matches) > 0:
        state.context['phone'] = matches[0]
        return True
    else:
        return False
