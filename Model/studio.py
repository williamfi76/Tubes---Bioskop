class Studio:
    def __init__(self, id, name, pricePerSeat:float, rows, columns):
        self.pricePerSeat = pricePerSeat
        self.id = id
        self.name = name
        self.row = rows
        self.column = columns

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
    
    def get_row(self):
        return self.row

    def set_row(self, value):
        self.row = value

    def get_column(self):
        return self.column

    def set_column(self, value):
        self.column = value