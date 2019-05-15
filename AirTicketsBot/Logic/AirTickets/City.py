import json;

class City:
     def __init__(self, code, name):
         self.code = code;
         self.name = name;

     @staticmethod
     def fromJson(jsonObj):
         obj = json.loads(jsonObj);
         return City(obj.get('code'), obj.get('name'));


