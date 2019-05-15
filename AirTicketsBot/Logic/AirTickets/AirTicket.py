import json;

class AirTicket:
     def __init__(self, obj):
         self.isActual = obj.get('actual');
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
         text += 'Дата вылета: ' + AirTicket.toStr(self.departDate) + '\r\n';
         text += 'Дата прилета: ' + AirTicket.toStr(self.returnDate) + '\r\n';
         text += 'Источник: ' + AirTicket.toStr(self.gate) + '\r\n';
         text += 'Дистанция: ' + AirTicket.toStr(self.distance) + 'км\r\n';

         if self.duration is not None:
             hours = self.duration / 60;
             minutes = self.duration - hours * 60;
             text += 'Время полета: ' + AirTicket.toStr(hours) + 'часов ' + AirTicket.toStr(minutes) +'минут\r\n';

         text += 'Количество трансферов: ' + AirTicket.toStr(self.transfers) + '\r\n';
         if self.tripClass is not None:
             if self.tripClass == 0:
                text += 'Эконом класс\r\n';
             if self.tripClass == 1:
                text += 'Бизнес класс\r\n';
             if self.tripClass == 2:
                text += 'Первый класс\r\n';
         text += '💰Цена: ' + AirTicket.toStr(self.price) + '\r\n';
         return text;

     @staticmethod
     def toStr(value):
         if value is None:
            return '-';
         return str(value);

