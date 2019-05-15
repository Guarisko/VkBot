from Database.Entities.DbUser import DbUser
from Database.Repositories.UserRepository import UserRepository
from vk_api.utils import get_random_id;
import vk_api;
from Logger import getLogger;

#Сессия для работы с ботов, предоставляет возможность отправлять сообщения с кнопками и без
class VkBotSession(BotSession):
      def __init__(self, baseSession: vk_api.VkApi):
         self.session = baseSession;
         self.logger = getLogger();
         self.user = None;

      def fromUserId(self, userId: int) -> None:
         self.userId = userId;

      def sendMsgKeyBoard(self, message: str, keyBoard: KeyBoard) -> None: 
         keyb = keyBoard.build();
         self.session.method('messages.send', {'user_id': self.userId, 'message': message, "random_id":get_random_id(), "keyboard": keyb});

      def sendMsg(self, message: str) -> None: 
         self.session.method('messages.send', {'user_id': self.userId, 'message': message, "random_id":get_random_id()});

      def sendMsgUser(self, message: str, userId: int) -> None: 
        self.session.method('messages.send', {'user_id': userId, 'message': message, "random_id":get_random_id()});

      def sendMsgKeyBoardUser(self, message: str, userId: int, keyBoard: KeyBoard) -> None: 
         keyb = keyBoard.build();
         self.session.method('messages.send', {'user_id': userId, 'message': message, "random_id":get_random_id(), "keyboard": keyb});

      def getUser(self) -> DbUser:
          foundUser = UserRepository.getById(self.userId);
          if foundUser:
             return foundUser;

          try:

            response = self.session.get_api().users.get(user_ids=[self.userId], fields=['domain'])[0];
            firstName = response['first_name'];
            lastName = response['last_name'];
            domain = 'https://vk.com/'+response['domain'];

            name = firstName + ' ' + lastName;
            UserRepository.save(self.userId, name, domain);

            self.user = DbUser(name=name, vkUrl= domain, vkUserId= self.userId);
            return self.user;
          except Exception as e:
              self.logger.fatal(e, exc_info=True);
              raise;


