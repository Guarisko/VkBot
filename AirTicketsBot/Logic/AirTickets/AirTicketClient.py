from Logic.AirTickets.AirTicket import AirTicket;
from Logic.AirTickets.City import City;
import requests;

#клиент для получения информации по авиабилетам работает через http api.travelpayouts
class AirTicketClient:
    def __init__(self):
        self.authToken = '7fd19706724df624fe13188104bcd310';
        self.baseUrl = 'https://api.travelpayouts.com';

        #cache cities for future requests
        cities = getJsonFromUrl('/data/cities.json');
        self.cities = [];
        for city in cities:
            self.cities.append(City.fromJson(city));

    def getCityByCode(self, code):
        return [t for t in self.cities if t.code == code];

    def getTickets(self, arrivalDate, departureDate, fromCity, toCity, currency):
        result = [];
        parameters = {
            'currency': currency,
            'depart_date': arrivalDate,
            'return_date': departureDate,
            'origin': fromCity,
            'destination': toCity,
            'show_to_affiliates': 'true'
        };
        jsonTickets = getJsonFromUrl('/v2/prices/nearest-places-matrix', parameters);
        for ticket in jsonTicket:
            result.append(AirTicket(ticket));
        return result;

    def getJsonFromUrl(self, url, parameters):
        headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/json;charset=utf-8',
            'X-Access-Token': self.authToken
        };
        r = requests.get(self.baseUrl + url, parameters=parameters, headers = headers);
        return r.json();


