from Model.role import Role


class Account:
    def __init__(self, id:int = 0, email:str = '', passwd:str='', role:Role = Role.MEMBER, pinNum:str=''):
        self.id = id
        self.email = email
        self.password = passwd
        self.role = role
        self.pin = pinNum

    def get_pin(self):
        return self.pin

    def set_pin(self, inputPin):
        self.pin = inputPin

    def get_id(self):
        return self.id

    def set_id(self, value):
        self.id = value

    def get_email(self):
        return self.email

    def set_email(self, value):
        self.email = value

    def get_password(self):
        return self.password

    def set_password(self, value):
        self.password = value

    def get_role(self):
        return self.role

    def set_role(self, value):
        self.role = value
