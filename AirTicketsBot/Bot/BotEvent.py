from Bot.Payload import Payload;

#Класс для хранения информации о событии из Бота
class BotEvent:
    def __init__(self, userId: int, message: str, payload = None):
         self.userId = userId;
         self.message = message;
         self.payload = Payload.fromJsonObject(payload);
