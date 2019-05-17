from peewee import *;
 
user = 'postgres';
password = '1';
db_name = 'hotels';
 
dbhandle = PostgresqlDatabase(
    db_name, user=user,
    password=password,
    host='localhost'
);

#работа с соединением в базе данных
class DbHandle:
    @staticmethod
    def get():
        dbhandle.connect(reuse_if_open=True);
        return dbhandle;


