class Studio:
    def __init__(self, rows, columns):
        self.seats = []
        for row in range(0, rows):
            rowSeats = []
            for column in range(0, columns):
                rowSeats.append("True")
            self.seats.append(rowSeats)
    
    def get_seats(self):
        return self.seats

    def set_seats(self, value):
        self.seats = value