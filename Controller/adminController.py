import re
import datetime
from typing import List
from Controller import mysqlConnector
from Controller import accountController
from Model.foodBeverageType import FoodBeverageType
from Model.movieStatus import MovieStatus
from Model.role import Role
from Model.genre import Genre
from Model.reviewFilm import ReviewFilm


def addNewShowing(movieId:int, startTime:datetime, endTime:datetime, studioId:int):
    try:
        db = mysqlConnector.connect()
        cursor = db.cursor()

        # Masukkan data Showing ke tabel food_beverage
        cursor.execute("""
            UPDATE movie SET status=1 where id = %s;
        """, (movieId,))

        cursor.execute("""
            INSERT INTO showing (movie_id, start_time, end_time, studio_id)
            VALUES (%s, %s, %s, %s);
        """, (movieId, startTime, endTime, studioId))

        db.commit()
        return True

    except Exception as e:
        db.rollback()
        return False

    finally:
        db.close()

def assignRoleToAccount(memberId:int, role:Role):
    try:
        db = mysqlConnector.connect()
        cursor = db.cursor()
        query = f"UPDATE account SET role={role.value} WHERE id={memberId}"
        cursor.execute(query)
        db.commit()
        return True

    except Exception as e:
        db.rollback()
        return False

    finally:
        db.close()

def addNewMovie(name:str, description:str, duration:int, genres: List[Genre] = [], status:MovieStatus = MovieStatus.NOT_SHOWING):
    try:
        db = mysqlConnector.connect()
        cursor = db.cursor()

        # Masukkan data film ke tabel movie
        
        posterPath = re.sub(r"[\'\";,.!?@#$%^&*]", "", name).lower().replace(" ", "_").replace(":", "-")
        posterPath += ".png"
        cursor.execute("""
            INSERT INTO movie (name, description, duration, poster_img_path, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, description, duration, posterPath, status.value))
        movie_id = cursor.lastrowid

        if len(genres) != 0:
            movie_genre = []
            for genre in genres:
                movie_genre.append(f"({movie_id}, {genre.value})")
            values_movie_genres = ", ".join(movie_genre)
            values_movie_genres += ";"
            print(values_movie_genres)
            query = f"INSERT INTO movie_genre (movie_id, genre_id) VALUES {values_movie_genres}"
            cursor.execute(query)

        db.commit()
        return True

    except Exception as e:
        db.rollback()
        return False

    finally:
        db.close()

def addNewFoodBeverage(name:str, fbType:FoodBeverageType, price:float = 0):
    try:
        db = mysqlConnector.connect()
        cursor = db.cursor()

        # Masukkan data Food/Beverage ke tabel food_beverage
        cursor.execute("""
            INSERT INTO food_beverage (name, type, price)
            VALUES (%s, %s, %s);
        """, (name, fbType.value, price))

        db.commit()
        return True

    except Exception as e:
        db.rollback()
        return False

    finally:
        db.close()

