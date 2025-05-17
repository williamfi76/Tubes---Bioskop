class Studio:
    def __init__(self, id, name, pricePerSeat:float, rows, columns):
        self.seats = []
        self.pricePerSeat = pricePerSeat
        self.id = id
        self.name = name
        for row in range(0, rows):
            rowSeats = []
            for column in range(0, columns):
                rowSeats.append("True")
            self.seats.append(rowSeats)

    def get_id(self):
        return self.id

    def set_id(self, value):
        self.id = value

    def get_name(self):
        return self.name

    def set_name(self, value):
        self.name = value

    def get_pricePerSeat(self):
        return self.pricePerSeat

    def set_pricePerSeat(self, value):
        self.pricePerSeat = value
    
    def get_seats(self):
        return self.seats

    def set_seats(self, value):
        self.seats = value