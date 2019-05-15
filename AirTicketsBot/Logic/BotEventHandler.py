from Bot.VkBotSession import VkBotSession
from Logic.ScreenRepository import ScreenRepository;
from Bot.BotEvent import BotEvent;
from Bot.VkBotKeyboard import VkBotKeyboard;
from Bot.VkBot import VkBot
from Logger import getLogger;

#обработчик событий от бота
class BotEventHandler:
    def __init__(self, session: VkBotSession):    
        self.logger = getLogger();
        self.botSession = session;
        self.screensRepository = ScreenRepository(session);
        self.screensRepository.initAll();

    def handle(self, event: BotEvent) -> None:
        try:
            foundScreen = self.screensRepository.getScreen(event);
            foundScreen.start();
        except Exception as e:
            self.handleError(e);

    def handleError(e):
        #сообщение об ошибке пользователю
        self.logger.fatal(e, exc_info=True);
        self.botSession.sendMsgUser('Произошла неизвестная ошибка.\r\nАдминистратор уже уведомлен.\r\nПеремещаю в основное меню');

        #сообщение об ошибке администратору
        user = self.botSession.getUser();
        VkBot.sendErrorToAdmin('Произошла неизвестная ошибка:' + str(e) + '\r\n пользователь: ' + str(user.url));

        #перемещение в основное меню
        mainScreen = self.screensRepository.mainScreen(self.botSession, VkBotKeyboard(), event);
        mainScreen.start();
        





