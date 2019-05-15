import json;

class AirTicket:
     def __init__(self, jsonObject):
         obj = json.loads(jsondata);
         isActual = obj.get('actual');
         self.departDate = obj.get('depart_date');
         self.returnDate = obj.get('return_date');
         self.gate = obj.get('gate');
         self.tripClass = obj.get('trip_class');
         self.transfers = obj.get('number_of_changes');
         self.distance = obj.get('distance');
         self.duration = obj.get('duration');
         self.price = obj.get('value');

     def getText(self):
         text = 'Авиабилет: '
         text += 'Дата вылета: ' + str(self.departDate) + '\r\n';
         text += 'Дата прилета: ' + str(self.returnDate) + '\r\n';
         text += 'Источник: ' + str(self.gate) + '\r\n';
         text += 'Дистанция: ' + str(self.distance) + 'км\r\n';

         hours = self.duration / 60;
         minutes = self.duration - hours * 60;
         text += 'Время полета: ' + str(self.hours) + 'часов ' + str(minutes) +'минут\r\n';

         text += 'Количество трансферов: ' + str(self.transfers) + '\r\n';
         if tripClass == 0:
            text += 'Эконом класс\r\n';
         if tripClass == 1:
            text += 'Бизнес класс\r\n';
         if tripClass == 2:
            text += 'Первый класс\r\n';
         text += '💰Цена: ' + str(self.price) + '\r\n';
         return text;

