from typing import List

from Model.movieStatus import MovieStatus
from Model.genre import Genre
from Model.reviewFilm import ReviewFilm

class Movie:
    def __init__(self, id: int, name:str, description:str, duration:int, poster:str, genre: List[Genre] = [], review:List[ReviewFilm] = [], status:MovieStatus = MovieStatus.NOT_SHOWING):
        self.id = id
        self.name = name
        self.description = description
        self.duration = duration
        self.poster = poster
        self.genre = genre
        self.review = review
        self.status = status

    def get_status(self):
        return self.status

    def set_status(self, value):
        self.status = value


    def get_id(self):
        return self.id

    def set_id(self, value):
        self.id = value

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
