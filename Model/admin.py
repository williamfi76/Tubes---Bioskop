from Model.account import Account
from Model.role import Role


class Admin(Account):
    def __init__(self, id = 0, email = '', passwd = '', pinNum = ''):
        super().__init__(id, email, passwd, Role.ADMIN, pinNum)
