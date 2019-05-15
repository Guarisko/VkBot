from Bot.KeyBoardButton import KeyBoardButton;
from vk_api.keyboard import VkKeyboard, VkKeyboardColor;

#Клавиатура вк бота, для упрощения работы с кнопками
class VkBotKeyboard:
      def __init__(self):
         self.keyboard = VkKeyboard(one_time=True);

      def addButton(self, button: KeyBoardButton) -> None:
          self.keyboard.add_button(label=button.text, color=VkKeyboardColor.DEFAULT, payload=button.payload.toJsonObject());

      def addNewLine(self) -> None:
          self.keyboard.add_line();

      def build(self) -> str:
          return self.keyboard.get_keyboard();

      def clear(self) -> None:
          self.keyboard = VkKeyboard(one_time=True);



