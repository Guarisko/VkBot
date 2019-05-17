from Bot.VkBotSession import VkBotSession
from Logger import getLogger;
from Logic.ScreenRepository import ScreenRepository;
from Bot.BotEvent import BotEvent;
from Bot.VkBotKeyboard import VkBotKeyboard;

#обработчик событий от бота
class BotEventHandler:
    def __init__(self, session: VkBotSession):    
        self.logger = getLogger();
        self.botSession = session;
        self.screensRepository = ScreenRepository(session);
        self.screensRepository.initAll();

    def handle(self, event: BotEvent) -> None:
        foundScreen = self.screensRepository.getScreen(event);
        foundScreen.start();