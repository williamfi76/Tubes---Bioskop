from Model.foodBeverageType import FoodBeverageType


class FoodBeverage:
    def __init__(self, id, name, fbType:FoodBeverageType, price:float):
        self.id = id
        self.name = name
        self.type = fbType
        self.price = price