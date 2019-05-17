class HotelPrice:
     def __init__(self, name, price, rates, fromCenter):
         self.name = name;
         self.price = price;
         self.rates = rates;
         self.fromCenter = fromCenter;

     def getText(self):
         text = 'Название: ' + self.name + '\r\n';
         text = '💰Цена: ' + str(self.price) + '\r\n';
         text = 'Количество отзывов: ' + str(self.rates) + '\r\n';
         text = 'Местоположение: ' + str(self.fromCenter) + '\r\n';
         return text;
