from Bot.VkBotSession import VkBotSession;
from Bot.Screen import Screen;
from Logic.Command import Command;
from Bot.Payload import Payload;
from Bot.KeyBoardButton import KeyBoardButton;
from Infrastructure.UserVariables import UserVariables;
from Bot.VkBotKeyboard import VkBotKeyboard;
from Bot.BotEvent import BotEvent;

import re;

#обобщение ввода пользователя
class InputScreen:
      def __init__(self, command, text, errorText, regex, saveVariable, nextCommand, nextScreen):
         self.text = text;
         self.command = command;
         self.errorText = errorText;
         self.regex = regex;
         self.saveVariable = saveVariable;
         self.nextCommand = nextCommand;
         self.nextScreen = nextScreen;

      def inputScreen(self, session: VkBotSession, keyBoard: VkBotKeyboard, event: BotEvent):
          userVars = UserVariables(event.userId);
          matches = re.findall(self.regex, event.message);
          screenText = self.text;
          foundCommand = userVars.getCommand();

          if foundCommand is not None and len(foundCommand) > 0:
              if len(matches) == 0 and foundCommand:
                 screenText = self.errorText;
              else:
                 userVars.addVariable(self.saveVariable, event.message);
                 userVars.addCommand('');
                 userVars.save();
                 return self.nextScreen(session, keyBoard, event);
          else:
             screenText = self.text;
             userVars.addCommand(self.command);
             userVars.save();
          keyBoard.addButton(KeyBoardButton('Назад в меню', Payload(Command.BackMenu)));
          return Screen( screenText, session, keyBoard);
