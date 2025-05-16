from Model.account import Account
from Model.role import Role


class Admin(Account):
    def __init__(self, id = 0, email = '', passwd = '', role = Role.ADMIN, pinNum = ''):
        super().__init__(id, email, passwd, role, pinNum)
