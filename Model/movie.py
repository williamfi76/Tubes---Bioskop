from typing import List

class Movie:
    def __init__(self, name:str, description:str, duration:int, poster:str, genre = []):
        self.name = name
        self.description = description
        self.duration = duration
        self.poster = poster
        self.genre = genre

    def get_name(self):
        return self.name

    def set_name(self, value):
        self.name = value

    def get_description(self):
        return self.description

    def set_description(self, value):
        self.description = value

    def get_duration(self):
        return self.duration

    def set_duration(self, value):
        self.duration = value

    def get_poster(self):
        return self.poster

    def set_poster(self, value):
        self.poster = value

    def get_genre(self):
        return self.genre

    def set_genre(self, value):
        self.genre = value
