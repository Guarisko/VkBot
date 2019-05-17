class HotelPrice:
     def __init__(self, name, price, rates, fromCenter):
         self.name = name;
         price2 = price;
         price2 = price2.replace('p.', '');
         price2 = price2.replace(' ', '');
         self.price = float(price2);
         self.rates = rates;
         self.fromCenter = fromCenter;

     def getText(self):
         text = 'Название: ' + self.getValue(self.name) + '\r\n';
         text += '💰Цена: ' + self.getValue(self.price) + '\r\n';
         text += self.getValue(self.rates) + '\r\n';
         text += 'Местоположение: ' + self.getValue(self.fromCenter) + '\r\n';
         return text;

     def getValue(self, value):
         if value is None:
            return '-';
         return str(value);