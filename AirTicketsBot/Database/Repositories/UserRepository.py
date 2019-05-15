from Logger import getLogger;
from Database.Entities.DbUser import DbUser;
from Database.DbHandle import DbHandle;
from Database.Entities.BaseDbModel import BaseDbModel;
from peewee import *;

#Repository для работы с пользователями
class UserRepository:
     @staticmethod
     def getById(userId):
        handle = DbHandle.get();
        result = None;
        try:
            result = DbUser.select().where(DbUser.vkUserId == userId).get();
        except Exception as e:
            getLogger().fatal(e, exc_info=True);
            result = None;
        finally:
            handle.close();
        return result;

     @staticmethod 
     def updateOrCreate(userId, name, url):
        handle = DbHandle.get();
        try:
            userExists = DbUser.select().where(DbUser.vkUserId == userId).exists();
            if not userExists:    
               user = DbUser(name=name, variables='{}', vkUserId = userId, vkUrl = url);
               user.save();
            else:
               u = DbUser.update(name=name, vkUrl = domain).where(DbUser.vkUserId == userId);
               u.execute();
        except Exception as e:
            getLogger().fatal(e, exc_info=True);
        finally:
            handle.close();

     @staticmethod 
     def updateVariables(userId, variables):
        handle = DbHandle.get();
        try:
          u = DbUser.update(variables=variables).where(DbUser.vkUserId == userId);
          u.execute();
        except Exception as e:
          getLogger().fatal(e, exc_info=True);
        finally:
          handle.close();