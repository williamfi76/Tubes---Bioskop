from datetime import datetime
from typing import List
from Controller.accountController import getFoodBeverageData
from Model.foodBeverage import FoodBeverage
from Model.foodBeverageStatus import FoodBeverageStatus
from Model.genre import Genre
from Model.member import Member
from Controller import mysqlConnector
from Model.movie import Movie
from Model.role import Role
from Model.showing import Showing
from Model.studio import Studio
from Model.ticket import Ticket
from Model.ticketStatus import TicketStatus
from Model.transactionFoodBeverage import TransactionFoodBeverage
from Model.transactionTicket import TransactionTicket

def getMovieGenre(idMovie:int):
    try:
        db = mysqlConnector.connect()
        cursor = db.cursor()
        query = """
            SELECT mg.genre_id
            FROM movie_genre as mg
            where movie_id=%s
        """
        cursor.execute(query, (idMovie,))
        genres:List[Genre] = []
        for data in cursor.fetchall():
            genres.append(Genre(data[0]))
        return genres
    except Exception as e:
        db.rollback()
        return []
    finally:
        db.close()

def getMovieData(idMovie:int):
    try:
        db = mysqlConnector.connect()
        cursor = db.cursor()
        query =  "SELECT m.id, m.name, m.description, m.duration, m.poster_img_path from movie as m where m.id=%s LIMIT 1"
        cursor.execute(query, (idMovie,))
        data = cursor.fetchone()
        movie = Movie(data[0], data[1], data[2], data[3], data[4],getMovieGenre(idMovie)) if cursor.rowcount != 0 else None
        return movie

    except Exception as e:
        db.rollback()
        return None

    finally:
        db.close()    

def getTicketsForShowing(trans_id:int):
    try:
        db = mysqlConnector.connect()
        cursor = db.cursor()
        tickets:List[Ticket] = []
        query =  "SELECT t.id, t.seat_name, t.trans_id from ticket as t where t.trans_id=%s"
        cursor.execute(query, (trans_id,))
        
        for data in cursor.fetchall():
            tickets.append(Ticket(data[0], data[1]))
        return tickets

    except Exception as e:
        db.rollback()
        return []

    finally:
        db.close()
    


def getAllMemberTicketTransactions(member: Member):
    transactions:List[TransactionTicket] = []
    try:
        db = mysqlConnector.connect()
        cursor = db.cursor()
        query = """  
            SELECT t.id, t.nominal, t.member_id, tt.showing_id, tt.ticket_status
            from transaction as t
            RIGHT JOIN transaction_ticket as tt ON t.id=tt.trans_id
            where t.member_id=%s
        """
        cursor.execute(query, (member.get_id(),))
        for data in cursor.fetchall():
            showing = getShowingData(data[3])
            tickets = getTicketsForShowing(data[0])
            transactions.append(TransactionTicket(data[0], tickets, member, showing, TicketStatus(data[4]),None))
        return transactions

    except Exception as e:
        print(e)
        db.rollback()
        return transactions
    finally:
        db.close()

def getShowingMovies():
    try:
        db = mysqlConnector.connect()
        cursor = db.cursor()
        showing:List[Showing]
        query = "SELECT m.id from movie as m where m.status=1"
        cursor.execute(query)
        movies:Movie = []
        for idMovies in cursor.fetchall():
            movies.append(getMovieData(idMovies[0]))
        return movies

    except Exception as e:
        db.rollback()
        return []
    finally:
        db.close()


def getMemberAllFoodBevereageTransactions(member: Member):
    transactions:List[TransactionFoodBeverage] = []
    try:
        db = mysqlConnector.connect()
        cursor = db.cursor()
        query = """  
            SELECT t.id, t.nominal, t.member_id, tt.showing_id, tt.ticket_status
            from transaction as t
            RIGHT JOIN transaction_ticket as tt ON t.id=tt.trans_id
            where t.member_id=%s
        """
        cursor.execute(query, (member.get_id(),))
        for data in cursor.fetchall():
            showing = getShowingData(data[3])
            tickets = getTicketsForShowing(data[0])
            transactions.append(TransactionTicket(data[0], tickets, member, showing, TicketStatus(data[4]),None))
        return transactions

    except Exception as e:
        print(e)
        db.rollback()
        return transactions
    finally:
        db.close()

def getMemberData(memberId:int):
    try:
        db = mysqlConnector.connect()
        cursor = db.cursor()
        query = "SELECT a.id, a.name, a.email, a.password, a.pinNum, a.role, m.wallet from account as a RIGHT JOIN member as m ON a.id = m.id WHERE id=%s AND a.role=%s LIMIT 1"
        cursor.execute(query, (memberId, Role.MEMBER.value))
        data = cursor.fetchone()
        member = Member(data[0], data[1], data[2], data[3],data[4], data[5])
        return member
    except Exception as e:
        db.rollback()
        return None
    finally:
        db.close()

def buyFoodBeverage(memberId:int, food_beverage_ids:List[int]):
    try:
        db = mysqlConnector.connect()
        cursor = db.cursor()
        items:List[FoodBeverage] = []
        for fbId in food_beverage_ids:
            items.append(getFoodBeverageData(fbId))
        totalPrice = 0
        for item in items:
            totalPrice += item.get_price()
        query_transaction = "INSERT INTO transaction (nominal, member_id) VALUES (%s, %s)"
        cursor.execute(query_transaction, (totalPrice, memberId))
        trans_id = cursor.lastrowid
        query_transaction = "INSERT INTO transaction_food_beverage (trans_id, status) VALUES (%s, %s)"
        cursor.execute(query_transaction, (trans_id, FoodBeverageStatus.UNREDEEMED.value))
        for item in items:
            query_transaction = "INSERT INTO order_food_beverage (trans_id, item) VALUES (%s, %s)"
            cursor.execute(query_transaction, (trans_id, item.get_id()))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(e)
        return False
    finally:
        db.close()

def buyTicket(memberId:int, idShowing: int, tickets:List[str]):
    try:
        db = mysqlConnector.connect()
        showing = getShowingData(idShowing)
        nominal = showing.get_studio().get_pricePerSeat() * len(tickets)
        cursor = db.cursor()
        query_transaction = "INSERT INTO transaction (nominal, member_id) VALUES (%s, %s)"
        cursor.execute(query_transaction, (nominal, memberId))
        transId = cursor.lastrowid
        review_query = """
            INSERT INTO review_film(movie_id, member_id, score, review)
            VALUES
            (%s, %s, %s, %s)
        """
        cursor.execute(review_query, (showing.get_movie().get_id(), memberId, 0, ""))
        reviewId = cursor.lastrowid
        query_trans_ticket = "INSERT INTO transaction_ticket (trans_id, ticket_status, review_id, showing_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(query_trans_ticket, (transId, TicketStatus.UNREDEEMED.value, reviewId, idShowing))

        query_tickets = """
            INSERT INTO ticket (trans_id, seat_name)
            VALUES
            (%s, %s)
        """
        for ticket in tickets:
            cursor.execute(query_tickets, (transId, ticket))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(e)
        return False
    finally:
        db.close()
    
def getStudioData(studioId):
    try:
        db = mysqlConnector.connect()
        cursor = db.cursor()
        query = "SELECT s.id, s.name, s.price_per_seat, s.row_count, s.column_count from studio as s where s.id = %s"
        cursor.execute(query, (studioId,))
        data = cursor.fetchone()
        return Studio(data[0], data[1], data[2], data[3], data[4])
    except Exception as e:
        db.rollback()
        return None
    finally:
        db.close()

def getShowingData(showingId:int):
    try:
        db = mysqlConnector.connect()
        cursor = db.cursor()
        query = "select s.id, s.movie_id, s.studio_id, s.start_time, s.end_time from showing as s where s.id=%s"
        cursor.execute(query, (showingId,))
        data = cursor.fetchone()
        currMovie = getMovieData(data[1])
        currStudio = getStudioData(data[2])
        showingData = Showing(data[0], currMovie, currStudio, datetime.strftime(data[3], "%Y-%m-%d %H:%M:%S"), datetime.strftime(data[4], "%Y-%m-%d %H:%M:%S") )
        return showingData
    except Exception as e:
        db.rollback()
        return None
    finally:
        db.close()