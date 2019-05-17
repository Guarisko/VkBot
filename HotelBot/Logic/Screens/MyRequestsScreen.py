from Bot.VkBotSession import VkBotSession;
from Logic.Screens.SearchTicketsScreen import searchHotels
from Logic.Variables import Variables;
from Database.Repositories.UserSearchRequestRepository import UserSearchRequestRepository;
from Bot.Screen import Screen;
from Logic.Command import Command;
from Bot.Payload import Payload;
from Bot.KeyBoardButton import KeyBoardButton;
from Infrastructure.UserVariables import UserVariables;
from Bot.VkBotKeyboard import VkBotKeyboard;
from Bot.BotEvent import BotEvent;

def myRequests(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    foundRequests = UserSearchRequestRepository.getByUserId(event.userId);
    for request in foundRequests:
        dict = {};
        dict['id']  = request.id;
        keyBoard.addButton(KeyBoardButton('С даты: ' + str(request.startDate) + ' в ' + str(request.city), Payload(Command.UserHotelsRequest, dict)));
        keyBoard.addNewLine();
    keyBoard.addButton(KeyBoardButton('Назад в меню', Payload(Command.BackMenu)));

    text = 'Здесь вы можете найти последние запросы и посмотреть доступны для них тарифы';
    if len(foundRequests) == 0 :
       text = 'Ни одного запроса не найдено.';
    screen = Screen( text, session, keyBoard);
    return screen;

def userHotelsRequestScreen(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    id = event.payload.dict['id'];
    request = UserSearchRequestRepository.getById(id);

    userVars = UserVariables(event.userId);
    userVars.addVariable(Variables.HotelFromDate, request.startDate);
    userVars.addVariable(Variables.HotelToDate, request.endDate);
    userVars.addVariable(Variables.HotelCity, request.city);
    userVars.addVariable(Variables.HotelGuests, request.guests);
    userVars.addVariable(Variables.HotelRooms, request.rooms);
    userVars.addVariable(Variables.PriceRange, request.priceRange);
    userVars.save();

    dict = {};
    dict['isSearch'] = True;
    event.payload.dict = dict;
    return searchHotels(session, keyBoard, event);
