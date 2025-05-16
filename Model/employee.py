from Model.account import Account
from Model.role import Role


class Employee(Account):
    def __init__(self, id = 0, email = '', passwd = '', role = Role.EMPLOYEE, pinNum = ''):
        super().__init__(id, email, passwd, role, pinNum)
