from Bot.Payload import Payload

#кнопка в боте
class KeyBoardButton:
      def __init__(self, text: str, payload: Payload):
         self.text = text;
         self.payload = payload;


