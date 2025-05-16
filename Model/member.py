from typing import List
from Model.account import Account
from Model.role import Role
from Model.transaction import Transaction


class Member(Account):
    def __init__(self, id = 0, email = '', passwd = '', pinNum = ''):
        super().__init__(id, email, passwd, Role.MEMBER, pinNum)
        self.wallet = 0.0
        self.transactions: List[Transaction] = []

    def get_wallet(self):
        return self.wallet

    def set_wallet(self, value):
        self.wallet = value

    def get_transactions(self):
        return self.transactions

    def set_transactions(self, value):
        self.transactions = value

