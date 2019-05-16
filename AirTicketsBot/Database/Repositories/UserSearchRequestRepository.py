from Database.Repositories.UserRepository import UserRepository
from Logger import getLogger;
from Database.Entities.DbUserSearchRequest import DbUserSearchRequest;
from Database.DbHandle import DbHandle;
from Database.Entities.BaseDbModel import BaseDbModel;
from peewee import *;

#Repository c запросами пользователей
class UserSearchRequestRepository:
     @staticmethod
     def getById(id):
        handle = DbHandle.get();
        result = None;
        try:
            result = DbUserSearchRequest.select().where(DbUserSearchRequest.id == id).get();
        except Exception as e:
            getLogger().fatal(e, exc_info=True);
            result = None;
        finally:
            handle.close();
        return result;

     @staticmethod
     def getByUserId(id):
        handle = DbHandle.get();
        result = [];
        try:
            user = UserRepository.getById(id);
            result = (DbUserSearchRequest.select()
                      .where(DbUserSearchRequest.user == user.id)
                      .limit(8)
                      .order_by(DbUserSearchRequest.createdMsk.desc())
                     );
        except Exception as e:
            getLogger().fatal(e, exc_info=True);
            result = [];
        finally:
            handle.close();
        return result;

     @staticmethod
     def create(currency, fromCity, toCity, startDate, endDate, userId):
        handle = DbHandle.get();
        try:
            user = UserRepository.getById(userId);
            request = DbUserSearchRequest(currency=currency, fromCity=fromCity, user=user.id, toCity=toCity,startDate=startDate, endDate=endDate);
            request.save();
        except Exception as e:
            getLogger().fatal(e, exc_info=True);
        finally:
            handle.close();