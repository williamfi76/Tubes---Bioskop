from Model.itemType import ItemType

class Transaction:
    def __init__(self, id, nominal, member:int):
        self.id = id
        self.nominal: float = nominal
        self.memberId = member

    def get_id(self):
        return self.id

    def set_id(self, value):
        self.id = value

    def get_nominal(self):
        return self.nominal

    def set_nominal(self, value):
        self.nominal = value

    def get_memberId(self):
        return self.memberId

    def set_memberId(self, value):
        self.memberId= value
