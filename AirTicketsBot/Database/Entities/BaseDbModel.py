from Database.DbHandle import DbHandle;
from peewee import *;

#базовая сущность для работы с ORM peewee
class BaseDbModel(Model):
    class Meta:
        database = DbHandle.get();