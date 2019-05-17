from Database.DbHandle import DbHandle
from Database.Repositories.UserRepository import UserRepository
from Logger import getLogger;
import json;

#класс для работы с переменными пользователя, нужен, чтобы возвращаться к состоянию, когда бот будет выключен
class UserVariables:
    def __init__(self, userId):
        self.variables = {};
        self.userId = userId;
        self.load();

    def getCommand(self):
        return self.getVariable('command');

    def addCommand(self, value):
        self.addVariable('command', value);

    def clear(self):
        self.variables = {};
        self.save();

    def getAll(self):
        return self.variables;

    def addVariable(self, variable, value):
        self.variables[variable] = value;

    def getVariable(self, variable):
        return self.variables.get(variable);

    def save(self):
        vars = json.dumps(self.variables);
        UserRepository.updateVariables(self.userId, vars);

    def load(self):
        handle = DbHandle.get();
        try:
            foundUser = UserRepository.getById(self.userId);
            if foundUser is not None and len(foundUser.variables) > 0:
               self.variables = json.loads(foundUser.variables);
        except Exception as e:
            self.variables = {};
        finally:
            handle.close();