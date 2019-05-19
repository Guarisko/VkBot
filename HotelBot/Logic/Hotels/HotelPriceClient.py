from Logic.Hotels.HotelPrice import HotelPrice
from Cache import getCache;
from Logger import getLogger;
import requests;

import time;

from selenium import webdriver;
from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.support import expected_conditions as EC;
from selenium.webdriver.common.by import By;
from selenium.webdriver.chrome.options import Options;
from selenium.common.exceptions import TimeoutException;
from fake_useragent import UserAgent;
import re;

#клиент для получения информации по отелям с помощью Selenium
class HotelPriceClient:

    def getHotels(self, arrivalDate, departureDate, city, guests, rooms):
        result = {
          'error':'',
          'hotels': []
        };
        try:
            result = self.enterData(arrivalDate, departureDate, city, guests, rooms);
        except Exception as e:
            getLogger().fatal(e, exc_info=True);
            result = {
                'error': 'Не удалось найти нужную информацию. Попробуйте еще раз',
                'hotels': []
            };
        return result;

    def getElement(self):
        options = Options()
        options.add_argument("--headless");
        options.add_argument('--no-sandbox');
        options.addArguments("--disable-dev-shm-usage");
        driver = webdriver.Chrome(chrome_options=options, executable_path='/usr/bin/chromedriver');
        driver.get('https://www.skyscanner.ru/hotels');

        delay = 45;
        tabs = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'HomePage_HomePage__searchSectionContent__3eAhc')))
        return driver;

    def enterData(self, arrivalDate, departureDate, city, guests, rooms):
        driver = self.getElement();

        inputElement = driver.find_element_by_id("destination-autosuggest")
        inputElement.send_keys(city);
        time.sleep(1);

        self.multiselect_set_selections(driver, 'adults', guests);
        time.sleep(1);
        self.multiselect_set_selections(driver, 'rooms', rooms);
        time.sleep(1);

        button = driver.find_element_by_xpath('//*[@id="search-controls"]/div[2]/button')
        button.click();

        url = driver.current_url;
        url = re.sub(r"checkin=\d{4}\-\d{2}\-\d{2}", "checkin=" + arrivalDate, url);
        url = re.sub(r"checkout=\d{4}\-\d{2}\-\d{2}", "checkout=" + departureDate, url);

        driver.get(url);
        time.sleep(1);
        driver.refresh();

        delay = 45;
        foundItems = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'HotelCardsListChunk_HotelCardsListChunk__card__1aNm2')))

        url = driver.current_url;
        error = '';
        hotels = [];
        if 'captcha' in url:
           error = 'К сожалению бот не смог получить информацию из-за блокировки :(';
        else:
           for element in driver.find_elements_by_class_name('HotelCardsListChunk_HotelCardsListChunk__card__1aNm2')[:8]:
               hotelName = self.tryGetElement(element, ".//div[@class='HotelCard_HotelCard__name__2jTNm']");
               price = self.tryGetElement(element, ".//div[@class='HotelCard_HotelCard__price__pZRWW']");
               fromCenter = self.tryGetElement(element, ".//p[@class='BpkText_bpk-text__nraB1 BpkText_bpk-text--sm__7CSMP HotelCard_HotelCard__distance__25Uru']");
               rate = self.tryGetElement(element, ".//span[@class='BpkText_bpk-text__nraB1 BpkText_bpk-text--sm__7CSMP']");
               hotels.append(HotelPrice(hotelName, price, rate, fromCenter));

        driver.close();
        return {
          'error':error,
          'hotels': hotels
        };

    def tryGetElement(self, element, path):
        text = '';
        try:
            text = element.find_element_by_xpath(path).text;
        except Exception as e:
           text = '';
        return text;

    def multiselect_set_selections(self, driver, element_id, labels):
        el = driver.find_element_by_id(element_id)
        for option in el.find_elements_by_tag_name('option'):
            if option.text in labels:
                option.click()


