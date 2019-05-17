from Bot.VkBotSession import VkBotSession
from Logic.Hotels.HotelPriceClient import HotelPriceClient
from Database.Repositories.UserSearchRequestRepository import UserSearchRequestRepository
from Cache import getCache;
from Logic.Variables import Variables;
from Bot.Screen import Screen;
from Logic.Command import Command
from Bot.Payload import Payload
from Bot.KeyBoardButton import KeyBoardButton
from Infrastructure.UserVariables import UserVariables;
from Bot.VkBotKeyboard import VkBotKeyboard;
from Bot.BotEvent import BotEvent;
import re;

import datetime;

def searchHotels(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    userVars = UserVariables(event.userId);
    
    client = HotelPriceClient();
    fromDate = userVars.getVariable(Variables.HotelFromDate);
    toDate = userVars.getVariable(Variables.HotelToDate);
    city = userVars.getVariable(Variables.HotelCity);
    guests = userVars.getVariable(Variables.HotelGuests);
    rooms = userVars.getVariable(Variables.HotelRooms);
    priceRange = userVars.getVariable(Variables.PriceRange);
    found = client.getHotels(fromDate, toDate, city, guests, rooms);

    isSearch = event.payload.dict['isSearch'];
    if not isSearch:
       UserSearchRequestRepository.create(city, guests, rooms, fromDate, toDate, priceRange, event.userId);

    error = found.get('error');
    hotels = found.get('hotels')[:8];
    
    cheapest = sorted(hotels, key=lambda x: x.price, reverse=False);

    if priceRange is not None:
        prices = priceRange.split();
        priceFrom = int(prices[0]);
        priceTo = int(prices[1]);
        cheapest = [item for item in cheapest if item.price >= priceFrom and item.price <= priceTo];

    userVars.clear();
    text = '';
    if len(error) > 0:
       text = error;
    else:
       if len(cheapest) == 0:
           text = 'К сожалению ничего не найдено:( Повторите запрос';
       else:
           text = 'Список дешевых отелей представлен ниже';
           idx = 0;
           getCache().set(event.userId, cheapest);
           for hotel in cheapest:
               textBtn = '💵 ' + str(hotel.price) + ' ' + str(hotel.name);
               dict = {};
               dict['idx'] = idx;
               keyBoard.addButton(KeyBoardButton(textBtn, Payload(Command.HotelInfo, dict)));
               keyBoard.addNewLine();
               idx+=1;

    keyBoard.addButton(KeyBoardButton('Назад в меню', Payload(Command.BackMenu)));
    screen = Screen( text, session, keyBoard);
    return screen;

def showHotelInfo(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    keyBoard.addButton(KeyBoardButton('Назад в меню', Payload(Command.BackMenu)));
    hotels = getCache().get(event.userId);
    idx = event.payload.dict['idx'];
    hotel = hotels[idx];
    data = hotel.getText();
    screen = Screen( data, session, keyBoard);
    return screen;

def searchHotelsFromDate(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    userVars = UserVariables(event.userId);
    matches = re.findall('\d{4}\-\d{2}\-\d{2}', event.message);
    screenText = 'Введите дату заезда (например 2019-07-01)';
    foundCommand = userVars.getCommand();

    if foundCommand is not None and len(foundCommand) > 0:
        if len(matches) == 0:
            screenText = 'Пожалуйста введите дату в следующем формате год-месяц-число';
        else:
            isCorrectDate = True;
            date = None;
            try:
                date = datetime.datetime.strptime(event.message, '%Y-%m-%d');
            except Exception as e:
                isCorrectDate = False;
            now = datetime.datetime.now();

            if isCorrectDate:
               isCorrectDate = (date.year >= now.year and date.month >= now.month and date.day > now.day) or ( date.year >= now.year and date.month > now.month);

            if isCorrectDate:
                userVars.addVariable(Variables.HotelFromDate, event.message);
                userVars.addCommand('');
                userVars.save();
                return searchHotelsToDate(session, keyBoard, event);
            else:
               screenText = 'Дата некорректная, должна быть больше чем сегодня например (2019-07-01)!';
    else:
        userVars.addCommand(Command.SearchHotelsFromDate);
        userVars.save();
    keyBoard.addButton(KeyBoardButton('Назад в меню', Payload(Command.BackMenu)));
    return Screen( screenText, session, keyBoard);

def searchHotelsToDate(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    userVars = UserVariables(event.userId);
    matches = re.findall('\d{4}\-\d{2}\-\d{2}', event.message);
    screenText = 'Введите дату выезда (например 2019-07-05)';
    foundCommand = userVars.getCommand();

    if foundCommand is not None and len(foundCommand) > 0:
        if len(matches) == 0:
            screenText = 'Пожалуйста введите дату в следующем формате год-месяц-число';
        else:

            fromDate = datetime.datetime.strptime(userVars.getVariable(Variables.HotelFromDate), '%Y-%m-%d');
            now = datetime.datetime.now();
            isCorrectDate = True;
            date = None;
            try:
                date = datetime.datetime.strptime(event.message, '%Y-%m-%d');
            except Exception as e:
                isCorrectDate = False;

            if isCorrectDate:
               isCorrectDate = (date.year >= now.year and date.month >= now.month and date.day > now.day) or ( date.year >= now.year and date.month > now.month);

            if isCorrectDate:
                if date > fromDate:
                    userVars.addVariable(Variables.HotelToDate, event.message);
                    userVars.addCommand('');
                    userVars.save();
                    return searchHotelsFromCity(session, keyBoard, event);
                else:
                    screenText = 'Дата должна быть больше чем дата заезда!';
            else:
                 screenText = 'Дата некорректная, должна быть больше чем сегодня например (2019-07-05)!';
    else:
        userVars.addCommand(Command.SearchHotelsToDate);
        userVars.save();
    keyBoard.addButton(KeyBoardButton('Назад в меню', Payload(Command.BackMenu)));
    return Screen( screenText, session, keyBoard);

def searchHotelsFromCity(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    userVars = UserVariables(event.userId);
    screenText = 'Куда вы поедете?';
    foundCommand = userVars.getCommand();
    matches = re.findall('^[a-zA-Zа-яА-Я]*$', event.message);

    if foundCommand is not None and len(foundCommand) > 0:
         if len(matches) == 0 or len(event.message) < 1:
            screenText = 'Пожалуйста введите название города';
         else:
            userVars.addVariable(Variables.HotelCity, event.message);
            userVars.addCommand('');
            userVars.save();
            return searchHotelsGuests(session, keyBoard, event);
    else:
        userVars.addCommand(Command.SearcHotelsCity);
        userVars.save();
    keyBoard.addButton(KeyBoardButton('Назад в меню', Payload(Command.BackMenu)));
    return Screen( screenText, session, keyBoard);

def searchHotelsGuests(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    userVars = UserVariables(event.userId);
    screenText = 'Количество человек (от 1 до 10)?';
    foundCommand = userVars.getCommand();

    if foundCommand is not None and len(foundCommand) > 0:
        if event.message not in ['1','2','3','4','5','6','7','8','9','10']:
           screenText = 'Пожалуйста введите число от 1 до 10';
        else:
            userVars.addVariable(Variables.HotelGuests, event.message);
            userVars.addCommand('');
            userVars.save();
            return searchHotelsRooms(session, keyBoard, event);
    else:
        userVars.addCommand(Command.SearchHotelsGuests);
        userVars.save();
    keyBoard.addButton(KeyBoardButton('Назад в меню', Payload(Command.BackMenu)));
    return Screen( screenText, session, keyBoard);

def searchHotelsRooms(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    userVars = UserVariables(event.userId);
    screenText = 'Количество комнат (от 1 до 5)?';
    foundCommand = userVars.getCommand();

    if foundCommand is not None and len(foundCommand) > 0:
        if event.message not in ['1', '2','3','4','5']:
           screenText = 'Пожалуйста введите число от 1 до 5';
        else:
            userVars.addVariable(Variables.HotelRooms, event.message);
            userVars.addCommand('');
            userVars.save();
            return searchHotelsPriceRange(session, keyBoard, event);
    else:
        userVars.addCommand(Command.SearchHotelsRooms);
        userVars.save();
    keyBoard.addButton(KeyBoardButton('Назад в меню', Payload(Command.BackMenu)));
    return Screen( screenText, session, keyBoard);

def searchHotelsPriceRange(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    userVars = UserVariables(event.userId);
    matches = re.findall('(\d+)\s(\d+)', event.message);
    screenText = 'Введите ценовой диапазон (10000 20000 только целые числа)';
    foundCommand = userVars.getCommand();

    if foundCommand is not None and len(foundCommand) > 0:
        if len(matches) == 0:
            screenText = 'Пожалуйста введите ценовой диапазон в следующем формате через пробел: 10000 20000';
        else:
            userVars.addVariable(Variables.PriceRange, event.message);
            userVars.addCommand('');
            userVars.save();
            dict ={};
            dict['isSearch'] = False;
            event.payload = Payload('', dict);
            return searchHotels(session, keyBoard, event);
    else:
        userVars.addCommand(Command.PriceRange);
        userVars.save();
    keyBoard.addButton(KeyBoardButton('Назад в меню', Payload(Command.BackMenu)));
    return Screen( screenText, session, keyBoard);
