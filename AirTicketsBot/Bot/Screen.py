from Bot.VkBotKeyboard import VkBotKeyboard;
from Bot.VkBotSession import VkBotSession;

#экран для работы с пользователем
class Screen:
    def __init__(self, text: str, botSession: VkBotSession, keyboard: VkBotKeyboard = None):
         self.text = text;
         self.keyboard = keyboard;
         self.session = botSession;

    def start(self) -> None:
        if self.keyboard is not None:
           self.session.sendMsgKeyBoard(self.text, self.keyboard);
        else:
           self.session.sendMsg(self.text);


