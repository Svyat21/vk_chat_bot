from flight_schedule import FLIGHTS, WEEKDAY
import datetime


class Dispatcer:

    def __init__(self):
        self.departure_cities = ''
        self.name_city_departure = ''
        self.destination_name_cities = ''
        self.destination_cities = None
        self.name_destination_city = ''
        self.departure_dates = None
        self.departure_day = None
        self.current_departure_dates = []

    def checking_city_of_departure(self, city):
        self.departure_cities = list(FLIGHTS.keys())
        if city in self.departure_cities:
            self.name_city_departure = city
            return True
        else:
            return False

    def checking_destination_city(self, city):
        self.destination_name_cities = list(FLIGHTS[self.name_city_departure].keys())
        self.destination_cities = FLIGHTS[self.name_city_departure]
        if city in self.destination_name_cities:
            self.name_destination_city = city
            return True
        else:
            return False

    def dey_generator(self):
        while True:
            yield self.departure_day
            self.departure_day += datetime.timedelta(days=1)

    def calculating_by_date(self):
        next_day = self.dey_generator()
        for i in next_day:
            if i.day in self.departure_dates:
                self.current_departure_dates.append(i)
            if len(self.current_departure_dates) == 5:
                break

    def calculations_by_day_of_week(self):
        next_day = self.dey_generator()
        for i in next_day:
            if WEEKDAY[i.weekday()] in self.departure_dates:
                self.current_departure_dates.append(i)
            if len(self.current_departure_dates) == 5:
                break

    def daily_departures(self):
        next_day = self.dey_generator()
        for index, i in enumerate(next_day):
            if index > 4:
                break
            self.current_departure_dates.append(i)

    def selection_nearest_flights(self, date):
        self.departure_day = date
        self.departure_dates = list(FLIGHTS[self.name_city_departure][self.name_destination_city]['Даты рейсов'])
        if isinstance(self.departure_dates[0], int):
            self.calculating_by_date()
        elif self.departure_dates[0] == 'ежедневно':
            self.daily_departures()
        else:
            self.calculations_by_day_of_week()

    def choosing_flight(self):
        pass
