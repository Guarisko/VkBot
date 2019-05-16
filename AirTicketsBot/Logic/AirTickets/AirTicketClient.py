from Cache import getCache;
from Logger import getLogger;
from Logic.AirTickets.AirTicket import AirTicket;
from Logic.AirTickets.City import City;
import requests;
import json;

#клиент для получения информации по авиабилетам работает через http api.travelpayouts
class AirTicketClient:
    def __init__(self):
        self.authToken = '7fd19706724df624fe13188104bcd310';
        self.baseUrl = 'https://api.travelpayouts.com';

    @staticmethod
    def initCities():
        cities = [];
        with open('cities.json', encoding="utf8") as json_file:  
            data = json.load(json_file).get('data');
            for city in data:
                cities.append(City.fromJson(city));
        getCache().set('cities', cities);
           

    @staticmethod
    def getCityByName(name):
        cities = getCache().get('cities');
        return [t for t in cities if name.lower() in t.name.lower()];

    @staticmethod
    def getCityByCode(code):
        cities = getCache().get('cities');
        return [t for t in cities if code in t.code];

    def getTickets(self, arrivalDate, departureDate, fromCity, toCity, currency):
        result = {
            'tickets': [],
            'error': ''
        };
        parameters = {
            'currency': currency,
            'depart_date': arrivalDate,
            'return_date': departureDate,
            'origin': fromCity,
            'destination': toCity,
            'show_to_affiliates': 'true'
        };
        try:
            jsonTickets = self.getJsonFromUrl('/v2/prices/nearest-places-matrix', parameters);
            data = jsonTickets.get('data');
            try:
                errors = data.get('errors');
                if errors is not None:
                   data = jsonTickets.get('data').get('prices');
            except Exception as e:
                data = jsonTickets.get('data').get('prices');

            for ticket in data:
                result['tickets'].append(AirTicket(ticket));
        except Exception as e:
            getLogger().fatal(e, exc_info=True);
            result['error'] = 'Вовремя поиска билетов произошла ошибка.\r\nСкорее всего вы указали неверные данные.\r\nВернитесь в меню и попробуйте снова.\r\n'
            raise;
        return result;

    def getJsonFromUrl(self, url, parameters):
        headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/json;charset=utf-8',
            'X-Access-Token': self.authToken
        };
        r = requests.get(self.baseUrl + url, params=parameters, headers = headers);
        return r.json();


