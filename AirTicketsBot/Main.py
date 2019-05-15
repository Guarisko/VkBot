from Bot.VkBot import VkBot;

# -*- coding: utf-8 -*-

from Database.DbSeed import DbSeed;
from Logger import getLogger;

import peewee;
import time;

def start():
    logger = getLogger();
    vkBot = VkBot();
    
    #перезапускает бота при ошибке через 60 секунд и отправляет сообщение администратору
    while True:
        try:
            DbSeed.init();
            logger.info('AirTickets bot started');
            vkBot.runListen();
            logger.info('AirTickets bot finished');
        except Exception as e:
            logger.fatal(e, exc_info=True);
            VkBot.sendErrorToAdmin('Ошибка при запуске приложения: ' + str(e));
            time.sleep(60);
            continue;

def main():
     start();

if __name__ == '__main__':
    main()
