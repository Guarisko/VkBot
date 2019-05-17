from Database.Entities.DbUser import DbUser;
from Database.Entities.BaseDbModel import BaseDbModel;
from peewee import *;
import datetime;

#cущность запроса на поиск отелей для конкретного пользователя
class DbUserSearchRequest(BaseDbModel):
    id = PrimaryKeyField(null=False);
    city = CharField(max_length=100);
    startDate = CharField(max_length=100);
    endDate = CharField(max_length=100);
    guests = IntegerField();
    rooms = IntegerField();
    createdMsk = DateTimeField(default=datetime.datetime.now);
    priceRange = CharField(max_length=100, null=True);
    user = ForeignKeyField(DbUser, related_name='fk_user_search_request_user_id', to_field='id');

    class Meta:
        db_table = "UserSearchRequests"