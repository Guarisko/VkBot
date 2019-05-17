from Bot.VkBotKeyboard import VkBotKeyboard;
from Logic.Variables import Variables;
from Logic.Screens.MyRequestsScreen import myRequests, userTicketRequestScreen;
from Logic.Screens.SearchTicketsScreen import searchTickets, selectCurrencyScreen, showTicketInfo, searchTicketsFromDate, searchTicketsToDate, searchTicketsFromDate, searchTicketsFromCity, searchTicketsToCity, searchTicketsFromCitySelect, searchTicketsToCitySelect, searchTicketsPriceRange;
from Logic.Command import Command
from Logic.Screens.MainScreen import mainScreen, backMenu, botRules, supportScreen, hotelsBot;
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

        self.screens[Command.SearchTicketsFromDate] = searchTicketsFromDate;
        self.screens[Command.SearchTicketsToDate] = searchTicketsToDate;

        self.screens[Command.SearchTicketsFromCity] = searchTicketsFromCity;
        self.screens[Command.SearchTicketsFromCitySelect] = searchTicketsFromCitySelect;

        self.screens[Command.PriceRange] = searchTicketsPriceRange;
        self.screens[Command.HotelsBot] = hotelsBot;
        
        self.screens[Command.SearchTicketsToCity] = searchTicketsToCity;
        self.screens[Command.SearchTicketsToCitySelect] = searchTicketsToCitySelect;
        
        self.screens[Command.SearchTicketsFromCurrency] = selectCurrencyScreen;

        self.screens[Command.SearchTickets] = searchTickets;
        self.screens[Command.UserRequests] = myRequests;
        self.screens[Command.UserTicketRequest] = userTicketRequestScreen;
        