from Bot.VkBotKeyboard import VkBotKeyboard
from Logic.Variables import Variables
from Logic.Screens.InputScreen import InputScreen;
from Logic.Screens.MyRequestsScreen import myRequests
from Logic.Screens.SearchTicketsScreen import searchTickets, selectCurrencyScreen, showTicketInfo;
from Logic.Command import Command
from Logic.Screens.MainScreen import mainScreen, backMenu, botRules, supportScreen;
from Bot.BotEvent import BotEvent;
from Database.DbHandle import DbHandle
from Bot.VkBotSession import VkBotSession;
from Infrastructure.UserVariables import UserVariables;

#Хранилище всех экранов
class ScreenRepository:
    def __init__(self, session: VkBotSession):    
        self.screens = {};
        self.mainScreen = None;
        self.session = session;

    #добавляет функцию основного экран в хранилище
    def addMain(self, screenFunc) -> None:
        self.mainScreen = screenFunc;

    #добавляет функцию экрана в хранилище
    def addScreen(self, command: str, screenFunc) -> None:
        self.screens[command] = screenFunc;

    #получает экран в зависимости от команды
    def getScreenByCommand(self, command: str) -> None:
        return self.screens.get(command);

    #получает экран по событию
    def getScreen(self, event: BotEvent) -> None:
        #если пользователь нажал кнопку и есть полезная нагрузка берем комманду и старуем экран
        if event.payload is not None and event.payload.command is not None:
           foundScreen = self.screens.get(event.payload.command);
           if foundScreen is not None:
               return foundScreen(self.session, VkBotKeyboard(), event);
        else:
            #если полезной нагрузки нет пытаемся стартовать команду, которую пользователь запускал последний раз
            handle = DbHandle.get();
            userVariables = UserVariables(event.userId);
            foundCommand = userVariables.getVariable('command');
            if foundCommand is not None:
                foundScreen = self.screens.get(foundCommand);
                #name = foundScreen.__name__;
                if foundScreen is not None:
                    handle.close();
                    return foundScreen(self.session, VkBotKeyboard(), event);
            handle.close();
        #если неизвестная команда перемещаем в основное меню
        return self.mainScreen(self.session, VkBotKeyboard(), event);

    #соответствие команд и функций выполнения экранов
    def initAll(self):
        self.mainScreen = mainScreen;

        self.screens[Command.BackMenu] = backMenu;
        self.screens[Command.Support] = supportScreen;
        self.screens[Command.BotRules] = botRules;
        self.screens[Command.TicketInfo] = showTicketInfo;


        currency = selectCurrencyScreen;
        toCity = InputScreen(Command.SearchTicketsToCity, 'В какой город вы поедете?','Введите корректный город', '(.*)', Variables.TicketFromCity, Command.SearchTicketsFromCurrency, currency).inputScreen;
        fromCity = InputScreen(Command.SearchTicketsFromCity, 'Из какого города вы поедете?','Введите корректный город', '(.*)', Variables.TicketToCity, Command.SearchTicketsToCity, toCity).inputScreen;
        toDate = InputScreen(Command.SearchTicketsToDate, 'Введите дату окончания поездки (2019-02-01)','Дата должна быть в формате 2019-02-01', '\d{4}\-\d{2}\-\d{2}', Variables.TicketToDate, Command.SearchTicketsFromCity, fromCity).inputScreen;
        fromDate = InputScreen(Command.SearchTicketsFromDate, 'Введите дату начала поездки (2019-02-01)','Дата должна быть в формате 2019-02-01', '\d{4}\-\d{2}\-\d{2}', Variables.TicketFromDate, Command.SearchTicketsToDate, toDate).inputScreen;

        self.screens[Command.SearchTicketsFromDate] = fromDate;
        self.screens[Command.SearchTicketsToDate] = toDate;
        self.screens[Command.SearchTicketsFromCity] = fromCity;
        self.screens[Command.SearchTicketsToCity] = toCity;
        self.screens[Command.SearchTicketsFromCurrency] = currency;

        self.screens[Command.SearchTickets] = searchTickets;
        self.screens[Command.UserRequests] = myRequests;