from Model.foodBeverageType import FoodBeverageType


class FoodBeverage:
    def __init__(self, id, name, fbType:FoodBeverageType, price:float):
        self.id = id
        self.name = name
        self.type = fbType
        self.price = price

    def get_id(self):
        return self.id

    def set_id(self, value):
        self.id = value

    def get_name(self):
        return self.name

    def set_name(self, value):
        self.name = value

    def get_type(self):
        return self.type

    def set_type(self, value):
        self.type = value

    def get_price(self):
        return self.price

    def set_price(self, value):
        self.price = value
