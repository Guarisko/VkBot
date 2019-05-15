from Bot.VkBotSession import VkBotSession
from Bot.Screen import Screen;
from Logic.Command import Command
from Bot.Payload import Payload
from Bot.KeyBoardButton import KeyBoardButton
from Infrastructure.UserVariables import UserVariables;
from Bot.VkBotKeyboard import VkBotKeyboard;
from Bot.BotEvent import BotEvent

def mainScreen(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    userVars = UserVariables(event.userId);
    userVars.clear();
   
    keyBoard.addButton(KeyBoardButton('Найти авиабилет', Payload(Command.SearchTickets)));
    keyBoard.addNewLine();

    keyBoard.addButton(KeyBoardButton('Мои запросы на поиск', Payload(Command.UserRequests)));
    keyBoard.addNewLine();

    keyBoard.addButton(KeyBoardButton('Поддержка', Payload(Command.Support)));
    keyBoard.addButton(KeyBoardButton('Как пользоваться ботом', Payload(Command.BotRules)));
    keyBoard.addNewLine();

    user = session.getUser();
    screen = Screen( user.name + ' , вас приветствует бот по поиску авиабилетов.\r\nВыберите подходящий пункт меню ниже.\r\nЕсли вы не видите пункты меню нажмите на квадратик рядом с полем ввода', session, keyBoard);
    return screen;

def supportScreen(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    keyBoard.addButton(KeyBoardButton('Назад в меню', Payload(Command.BackMenu)));
    screen = Screen('Для технической поддержки напишите администратору группы. Перейдите по ссылке: https://vk.com/club153941379', session, keyBoard);
    return screen;

def botRules(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    keyBoard.addButton(KeyBoardButton('Назад в меню', Payload(Command.BackMenu)));
    screen = Screen( 'Для того чтобы найти авиабилет нажмите кнопку "Найти авиабилет" в главном меню и следуйте указаниям бота.\r\nВсе ваши запросы на поиск будут сохраняться и вы сможете найти их с помощью кнопки "Мои запросы на поиск"', session, keyBoard);
    return screen;

def backMenu(session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
    return mainScreen(session, keyBoard, event);