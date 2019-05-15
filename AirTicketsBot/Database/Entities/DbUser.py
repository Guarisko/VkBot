from Database.Entities.BaseDbModel import BaseDbModel;
from peewee import *;

#cущность пользователя
class DbUser(BaseDbModel):
    id = PrimaryKeyField(null=False);
    name = CharField(max_length=100);
    vkUserId = IntegerField(null=False);
    variables = TextField();
    vkUrl = TextField();

    class Meta:
        db_table = "UserSettings"