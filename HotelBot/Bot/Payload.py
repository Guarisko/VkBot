import json;

#Полезная нагрузка, которую можно засунуть в кнопку, информация придет от вк при нажатии кнопки, хранится в json для удобства
class Payload:
    def __init__(self, command: str, dict = None):
         self.command = command;
         self.dict = dict;

    @staticmethod
    def fromJsonObject(jsondata):
        if jsondata is not None and len(jsondata) > 0:
            obj = json.loads(jsondata);
            command = obj.get('command');
            dict = obj.get('dict');
            return Payload(command, dict);
        return None;

    def toJsonObject(self):
        result = {};
        if self.command is not None and len(self.command) > 0:
           result['command'] = self.command;
        if self.dict is not None:
           result['dict'] = self.dict;
        return result;


