from Model.itemType import ItemType

class Transaction:
    def __init__(self, id, nominal, itemType:ItemType = ItemType.MOVIE, memberId:int = 0):
        self.id = id
        self.nominal: float = nominal
        self.memberId: int
        self.type:ItemType = itemType

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

    def get_type(self):
        return self.type

    def set_type(self, value):
        self.type:ItemType = value
