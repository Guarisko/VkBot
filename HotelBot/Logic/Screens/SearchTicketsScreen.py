from Bot.VkBotSession import VkBotSession
from Database.Repositories.UserSearchRequestRepository import UserSearchRequestRepository
from Cache import getCache
from Logic.Variables import Variables
from Logic.AirTickets.AirTicketClient import AirTicketClient;
from Bot.Screen import Screen;
from Logic.Command import Command
from Bot.Payload import Payload
from Bot.KeyBoardButton import KeyBoardButton
from Infrastructure.UserVariables import UserVariables;
from Bot.VkBotKeyboard import VkBotKeyboard;
from Bot.BotEvent import BotEvent;
import re;

import datetime;

def searchTickets(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    userVars = UserVariables(event.userId);
    
    client = AirTicketClient();
    fromDate = userVars.getVariable(Variables.TicketFromDate);
    toDate = userVars.getVariable(Variables.TicketToDate);
    fromCity = userVars.getVariable(Variables.TicketFromCity);
    toCity = userVars.getVariable(Variables.TicketToCity);
    priceRange = userVars.getVariable(Variables.PriceRange);
    currency = event.payload.dict['currency'];
    found = client.getTickets(fromDate, toDate, fromCity, toCity, currency);

    isSearch = event.payload.dict['isSearch'];
    if not isSearch:
       UserSearchRequestRepository.create(currency, fromCity, toCity, fromDate, toDate,priceRange, event.userId);

    error = found.get('error');
    tickets = found.get('tickets')[:8];

    
    cheapest = sorted(tickets, key=lambda x: x.price, reverse=False);

    if priceRange is not None:
        prices = priceRange.split();
        priceFrom = int(prices[0]);
        priceTo = int(prices[1]);
        cheapest = [item for item in cheapest if item.price >= priceFrom and item.price <= priceTo];

    userVars.addVariable('currency', currency);

    userVars.clear();
    text = '';
    if len(error) > 0:
       text = error;
    else:
       if len(cheapest) == 0:
           text = 'К сожалению ничего не найдено:( Повторите запрос';
       else:
           text = 'Список дешевых авиабилетов представлен ниже';
           idx = 0;
           getCache().set(event.userId, cheapest);
           for ticket in cheapest:
               textBtn = '💵 ' + str(ticket.price) + ' ' + str(ticket.gate);
               dict = {};
               dict['idx'] = idx;
               dict['currency'] = currency;
               keyBoard.addButton(KeyBoardButton(textBtn, Payload(Command.TicketInfo, dict)));
               keyBoard.addNewLine();
               idx+=1;

    keyBoard.addButton(KeyBoardButton('Назад в меню', Payload(Command.BackMenu)));
    screen = Screen( text, session, keyBoard);
    return screen;

def showTicketInfo(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    keyBoard.addButton(KeyBoardButton('Назад в меню', Payload(Command.BackMenu)));
    tickets = getCache().get(event.userId);
    idx = event.payload.dict['idx'];
    currency = event.payload.dict['currency'];
    ticket = tickets[idx];
    data = ticket.getText() + '\r\nВалюта: ' + currency.upper();
    screen = Screen( data, session, keyBoard);
    return screen;

def selectCurrencyScreen(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    userVars = UserVariables(event.userId);

    dictRub = {};
    dictRub['currency'] = 'rub';
    dictRub['isSearch'] = False;

    dictKzt = {};
    dictKzt['currency'] = 'kzt';
    dictKzt['isSearch'] = False;

    dictUsd = {};
    dictUsd['currency'] = 'usd';
    dictUsd['isSearch'] = False;

    dictEur = {};
    dictEur['currency'] = 'eur';
    dictEur['isSearch'] = False;

    keyBoard.addButton(KeyBoardButton('RUB', Payload(Command.SearchTickets, dictRub)));
    keyBoard.addNewLine();
    keyBoard.addButton(KeyBoardButton('USD', Payload(Command.SearchTickets, dictUsd)));
    keyBoard.addNewLine();
    keyBoard.addButton(KeyBoardButton('EUR', Payload(Command.SearchTickets, dictEur)));
    keyBoard.addNewLine();
    keyBoard.addButton(KeyBoardButton('KZT', Payload(Command.SearchTickets, dictKzt)));
    screen = Screen( 'Выберите валюту для поиска билетов', session, keyBoard);
    return screen;

def searchTicketsFromDate(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    userVars = UserVariables(event.userId);
    matches = re.findall('\d{4}\-\d{2}\-\d{2}', event.message);
    screenText = 'Введите дату начала поездки (например 2019-07-01)';
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
                userVars.addVariable(Variables.TicketFromDate, event.message);
                userVars.addCommand('');
                userVars.save();
                return searchTicketsToDate(session, keyBoard, event);
            else:
               screenText = 'Дата некорректная, должна быть больше чем сегодня например (2019-07-01)!';
    else:
        userVars.addCommand(Command.SearchTicketsFromDate);
        userVars.save();
    keyBoard.addButton(KeyBoardButton('Назад в меню', Payload(Command.BackMenu)));
    return Screen( screenText, session, keyBoard);

def searchTicketsToDate(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    userVars = UserVariables(event.userId);
    matches = re.findall('\d{4}\-\d{2}\-\d{2}', event.message);
    screenText = 'Введите дату окончания поездки (например 2019-07-05)';
    foundCommand = userVars.getCommand();

    if foundCommand is not None and len(foundCommand) > 0:
        if len(matches) == 0:
            screenText = 'Пожалуйста введите дату в следующем формате год-месяц-число';
        else:

            fromDate = datetime.datetime.strptime(userVars.getVariable(Variables.TicketFromDate), '%Y-%m-%d');
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
                    userVars.addVariable(Variables.TicketToDate, event.message);
                    userVars.addCommand('');
                    userVars.save();
                    return searchTicketsFromCity(session, keyBoard, event);
                else:
                    screenText = 'Дата должна быть больше чем дата начала поездки!';
            else:
                 screenText = 'Дата некорректная, должна быть больше чем сегодня например (2019-07-05)!';
    else:
        userVars.addCommand(Command.SearchTicketsToDate);
        userVars.save();
    keyBoard.addButton(KeyBoardButton('Назад в меню', Payload(Command.BackMenu)));
    return Screen( screenText, session, keyBoard);

def searchTicketsFromCity(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    userVars = UserVariables(event.userId);
    screenText = 'Откуда вы поедете?';
    foundCommand = userVars.getCommand();

    if foundCommand is not None and len(foundCommand) > 0:
        cities = AirTicketClient.getCityByName(event.message);
        if cities is None or len(cities) == 0:
           screenText = 'К сожалению ни один город не найден.';
        else:
            screenText = 'Выберите найденный город из списка';
            firstCities = cities[:7];

            filteredCities = [];
            foundNames = [];
            for city in firstCities:
                if city.name not in foundNames:
                   foundNames.append(city.name);
                   filteredCities.append(city);

            for c in filteredCities:
                dict = {};
                dict['code'] = c.code;
                dict['name'] = c.name;
                keyBoard.addButton(KeyBoardButton(c.name, Payload(Command.SearchTicketsFromCitySelect, dict)));
                keyBoard.addNewLine();
    else:
        userVars.addCommand(Command.SearchTicketsFromCity);
        userVars.save();
    keyBoard.addButton(KeyBoardButton('Назад в меню', Payload(Command.BackMenu)));
    return Screen( screenText, session, keyBoard);

def searchTicketsFromCitySelect(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    code = event.payload.dict['code'];
    name = event.payload.dict['name'];
    userVars = UserVariables(event.userId);
    userVars.addVariable(Variables.TicketFromCity, code);
    userVars.addVariable(Variables.TicketFromCityName, name);
    userVars.addCommand('');
    userVars.save();
    return searchTicketsToCity(session, keyBoard, event);

def searchTicketsToCity(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    userVars = UserVariables(event.userId);
    screenText = 'Куда вы поедете?';
    foundCommand = userVars.getCommand();

    if foundCommand is not None and len(foundCommand) > 0:
        cities = AirTicketClient.getCityByName(event.message);
        if cities is None or len(cities) == 0:
           screenText = 'К сожалению ни один город не найден.';
        else:
            screenText = 'Выберите найденный город из списка';
            firstCities = cities[:7];

            filteredCities = [];
            foundNames = [];
            for city in firstCities:
                if city.name not in foundNames:
                   foundNames.append(city.name);
                   filteredCities.append(city);

            for c in filteredCities:
                dict = {};
                dict['code'] = c.code;
                dict['name'] = c.name;
                keyBoard.addButton(KeyBoardButton(c.name, Payload(Command.SearchTicketsToCitySelect, dict)));
                keyBoard.addNewLine();
    else:
        userVars.addCommand(Command.SearchTicketsToCity);
        userVars.save();
    keyBoard.addButton(KeyBoardButton('Назад в меню', Payload(Command.BackMenu)));
    return Screen( screenText, session, keyBoard);

def searchTicketsToCitySelect(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    code = event.payload.dict['code'];
    name = event.payload.dict['name'];
    userVars = UserVariables(event.userId);
    userVars.addVariable(Variables.TicketToCity, code);
    userVars.addVariable(Variables.TicketToCityName, name);
    userVars.addCommand('');
    userVars.save();
    return searchTicketsPriceRange(session, keyBoard, event);

def searchTicketsPriceRange(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
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
            return selectCurrencyScreen(session, keyBoard, event);
    else:
        userVars.addCommand(Command.PriceRange);
        userVars.save();
    keyBoard.addButton(KeyBoardButton('Назад в меню', Payload(Command.BackMenu)));
    return Screen( screenText, session, keyBoard);
