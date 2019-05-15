#coding=utf-8
from Database.DbHandle import DbHandle;
from Database.Entities.DbUserSearchRequest import DbUserSearchRequest;
from Database.Entities.DbUser import DbUser;

import peewee;
#создает таблицы в базе данных, если они не существуют
class DbSeed:
    
    @staticmethod
    def init():
        handle = DbHandle.get();
        DbUser.create_table();
        DbUserSearchRequest.create_table();
        handle.close();

