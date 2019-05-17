'''
- Класс для прослушивания сообщений ВкБота через LongPolling Api
'''
from Logic.BotEventHandler import BotEventHandler
from Bot.VkBotKeyboard import VkBotKeyboard
from Bot.VkBotSession import VkBotSession
from Bot.BotEvent import BotEvent

from Config import *;
from vk_api.longpoll import VkLongPoll, VkEventType;

import vk_api;

class VkBot:
    #начинает слушать сообщения от вк бота и принимать только те которые ему отправил пользователь
    def runListen(self):
        vk_session = vk_api.VkApi(token=VK_BOT_TOKEN);
        longpoll = VkLongPoll(vk_session);
        
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    text = event.text;

                    payload = '';
                    if hasattr(event, 'payload'):
                       payload = event.payload;

                    botSession = VkBotSession(vk_session);
                    eventHandler = BotEventHandler(botSession);
                    botEvent = BotEvent(event.user_id, text, payload);
                    botSession.fromUserId(botEvent.userId);
                    botSession.getUser();
                    try:
                        eventHandler.handle(botEvent);
                    except Exception as e:
                        #сообщение об ошибке пользователю
                        eventHandler.logger.fatal(e, exc_info=True);
                        eventHandler.botSession.sendMsgUser('Произошла неизвестная ошибка.\r\nАдминистратор уже уведомлен.\r\nПеремещаю в основное меню', botEvent.userId);

                        #сообщение об ошибке администратору
                        user = eventHandler.botSession.getUser();
                        self.sendErrorToAdmin('Произошла неизвестная ошибка:' + str(e) + '\r\n пользователь: ' + str(user.vkUrl));

                        #перемещение в основное меню
                        mainScreen = eventHandler.screensRepository.mainScreen(eventHandler.botSession, VkBotKeyboard(), event);
                        mainScreen.start();

    #отправляет сообщение об ошибке администратору
    @staticmethod
    def sendErrorToAdmin(msg):
        vk_session = vk_api.VkApi(token=VK_BOT_TOKEN);
        botSession = VkBotSession(vk_session);
        botSession.sendMsgUser(str(msg), ADMIN_VK_USER_ID);
                    
        