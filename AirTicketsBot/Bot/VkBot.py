'''
- Класс для прослушивания сообщений ВкБота через LongPolling Api
'''
from Logic.BotEventHandler import BotEventHandler
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
                    eventHandler.handle(botEvent);

    #отправляет сообщение об ошибке администратору
    @staticmethod
    def sendErrorToAdmin(msg):
        vk_session = vk_api.VkApi(token=VK_BOT_TOKEN);
        botSession = VkBotSession(vk_session);
        botSession.sendMsgUser(str(msg), ADMIN_VK_USER_ID);
                    
        