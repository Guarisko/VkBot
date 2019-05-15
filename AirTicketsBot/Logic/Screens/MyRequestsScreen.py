from Bot.VkBotSession import VkBotSession
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
        keyBoard.addButton(KeyBoardButton('В разработке', Payload(Command.BackMenu)));
        keyBoard.addNewLine();
    keyBoard.addButton(KeyBoardButton('Назад в меню', Payload(Command.BackMenu)));
    text = 'Вам доступны последние 9 запросов на поисков нажмите на кнопку, чтобы выбрать необходимый';
    if len(foundRequests) == 0 :
       text = 'Ни одного запроса не найдено.';
    screen = Screen( text, session, keyBoard);
    return screen;