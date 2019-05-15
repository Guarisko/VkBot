from Database.Entities.DbUser import DbUser;
from Database.Entities.BaseDbModel import BaseDbModel;
from peewee import *;

#cущность запроса на поиск авиабилетов для конкретного пользователя
class DbUserSearchRequest(BaseDbModel):
    id = PrimaryKeyField(null=False);
    currency = CharField(max_length=100);
    fromCountry = CharField(max_length=100);
    toCountry = CharField(max_length=100);
    startDate = CharField(max_length=100);
    endDate = CharField(max_length=100);
    user = ForeignKeyField(DbUser, related_name='fk_user_search_request_user_id', to_field='id');

    class Meta:
        db_table = "UserSearchRequests"