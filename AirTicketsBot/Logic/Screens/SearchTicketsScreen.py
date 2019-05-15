from Bot.VkBotSession import VkBotSession
from Cache import getCache
from Logic.Variables import Variables
from Logic.AirTickets.AirTicketClient import AirTicketClient;
from Bot.Screen import Screen;
from Logic.Command import Command
from Bot.Payload import Payload
from Bot.KeyBoardButton import KeyBoardButton
from Infrastructure.UserVariables import UserVariables;
from Bot.VkBotKeyboard import VkBotKeyboard;
from Bot.BotEvent import BotEvent

def searchTickets(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    userVars = UserVariables(event.userId);
    
    client = AirTicketClient();
    fromDate = userVars.getVariable(Variables.TicketFromDate);
    toDate = userVars.getVariable(Variables.TicketToDate);
    currency = event.payload.dict['currency'];
    found = client.getTickets(fromDate, toDate, 'LED', 'HKT', currency);
    error = found.get('error');
    tickets = found.get('tickets')[:9];
    cheapest = sorted(tickets, key=lambda x: x.price, reverse=False);

    userVars.addVariable('currency', currency);
    getCache().set(str(event.userId) + '_variables', userVars.getAll());
    userVars.clear();
    text = '';
    if len(error) > 0:
       text = error;
    else:
       if len(cheapest) == 0:
           text = 'К сожалению ничего не найдено:( Повторите запрос';
       else:
           text = 'Список дешевых авиабилетов представлен ниже';
           for ticket in cheapest:
               getCache().set(event.userId, ticket);
               textBtn = '💵 ' + str(ticket.price) + ' ' + str(ticket.gate);
               keyBoard.addButton(KeyBoardButton(textBtn, Payload(Command.TicketInfo)));
               keyBoard.addNewLine();

    keyBoard.addButton(KeyBoardButton('Назад в меню', Payload(Command.BackMenu)));
    screen = Screen( text, session, keyBoard);
    return screen;

def showTicketInfo(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    keyBoard.addButton(KeyBoardButton('Назад в меню', Payload(Command.BackMenu)));
    ticket = getCache().get(event.userId);
    variables = getCache().get(str(event.userId) + '_variables');
    data = ticket.getText();
    screen = Screen( data, session, keyBoard);
    return screen;

def selectCurrencyScreen(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    userVars = UserVariables(event.userId);

    dictRub = {};
    dictRub['currency'] = 'rub';

    dictKzt = {};
    dictKzt['currency'] = 'kzt';

    dictUsd = {};
    dictUsd['currency'] = 'usd';

    dictEur = {};
    dictEur['currency'] = 'eur';

    keyBoard.addButton(KeyBoardButton('RUB', Payload(Command.SearchTickets, dictRub)));
    keyBoard.addNewLine();
    keyBoard.addButton(KeyBoardButton('USD', Payload(Command.SearchTickets, dictUsd)));
    keyBoard.addNewLine();
    keyBoard.addButton(KeyBoardButton('EUR', Payload(Command.SearchTickets, dictEur)));
    keyBoard.addNewLine();
    keyBoard.addButton(KeyBoardButton('KZT', Payload(Command.SearchTickets, dictKzt)));
    screen = Screen( 'Выберите валюту для поиска билетов', session, keyBoard);
    return screen;