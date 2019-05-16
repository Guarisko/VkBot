import json;

class City:
     def __init__(self, code, name):
         self.code = code;
         self.name = name;

     @staticmethod
     def fromJson(jsonObj):
         return City(jsonObj.get('code'), jsonObj.get('name'));

     def toJson(self):
         result = {
             "code": self.code,
             "name": self.name
         };
         return result;

