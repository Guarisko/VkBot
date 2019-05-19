from peewee import *;
 
user = 'postgres';
password = '12345678';
db_name = 'hotels';
 
dbhandle = PostgresqlDatabase(
    db_name, user=user,
    password=password,
    host='185.185.69.252'
);

#работа с соединением в базе данных
class DbHandle:
    @staticmethod
    def get():
        dbhandle.connect(reuse_if_open=True);
        return dbhandle;


