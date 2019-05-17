from Cache import getCache;
from Logger import getLogger;
import requests;
import json;

#клиент для получения информации по отелям с помощью Selenium
class HotelPriceClient:

    def getHotels(self, arrivalDate, departureDate, city, guests, rooms):
        result = {
          'error':'',
          'hotels': []
        };
        return result;


