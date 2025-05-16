import datetime
from Model.movie import Movie
from Model.showing import Showing

class Ticket:
    def __init__(self,id:int , seatName, showing:Showing, redeem:bool = False):
        self.id = id
        self.seatName = seatName
        self.redeem:bool = redeem
        self.showing = showing

    def get_id(self):
        return self.id

    def set_id(self, value):
        self.id = value

    def get_seatName(self):
        return self.seatName

    def set_seatName(self, value):
        self.seatName = value

    def get_redeem(self):
        return self.redeem

    def set_redeem(self, value):
        self.redeem = value

    def get_showing(self):
        return self.showing

    def set_showing(self, value):
        self.showing = value

