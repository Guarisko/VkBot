from Bot.VkBotSession import VkBotSession
from Logic.Screens.SearchTicketsScreen import searchTickets
from Logic.Variables import Variables
from Logic.AirTickets.AirTicketClient import AirTicketClient;
from Database.Repositories.UserSearchRequestRepository import UserSearchRequestRepository
from Bot.Screen import Screen;
from Logic.Command import Command
from Bot.Payload import Payload
from Bot.KeyBoardButton import KeyBoardButton
from Infrastructure.UserVariables import UserVariables;
from Bot.VkBotKeyboard import VkBotKeyboard;
from Bot.BotEvent import BotEvent

def myRequests(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    foundRequests = UserSearchRequestRepository.getByUserId(event.userId);
    for request in foundRequests:
        city = AirTicketClient.getCityByCode(request.fromCity)[0];
        name = city.name[0:20];
        dict = {};
        dict['id']  = request.id;
        keyBoard.addButton(KeyBoardButton('С даты: ' + str(request.startDate) + '❗ из ' + str(name), Payload(Command.UserTicketRequest, dict)));
        keyBoard.addNewLine();
    keyBoard.addButton(KeyBoardButton('Назад в меню', Payload(Command.BackMenu)));

    text = 'Здесь вы можете найти последние запросы и посмотреть доступны для них билеты';
    if len(foundRequests) == 0 :
       text = 'Ни одного запроса не найдено.';
    screen = Screen( text, session, keyBoard);
    return screen;

def userTicketRequestScreen(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    id = event.payload.dict['id'];
    request = UserSearchRequestRepository.getById(id);

    userVars = UserVariables(event.userId);
    userVars.addVariable(Variables.TicketFromDate, request.startDate);
    userVars.addVariable(Variables.TicketToDate, request.endDate);
    userVars.addVariable(Variables.TicketFromCity, request.fromCity);
    userVars.addVariable(Variables.TicketToCity, request.toCity);
    userVars.addVariable(Variables.PriceRange, request.priceRange);
    userVars.save();

    dict = {};
    dict['currency'] = request.currency;
    dict['isSearch'] = True;
    event.payload.dict = dict;
    return searchTickets(session, keyBoard, event);
