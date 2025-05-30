from datetime import datetime
from typing import List

from flask import Blueprint, app, redirect, render_template, request, session, url_for
from Controller import accountController
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

member_bp = Blueprint('member', __name__, url_prefix='/member')

@member_bp.route("/redeem/<int:trans_id>", methods=["GET", "POST"])
def redeemTicket(trans_id):
    if "id" not in session:
        return redirect(url_for("logout"))
    trans = getSingleTransaction(trans_id)
    if session["id"] != trans.get_memberId():
        return redirect(url_for("logout"))
    if request.method == "POST":
        if redeemSingleTransaction(trans_id):
            return redirect(url_for("member.showMemberTicketData"))
    showing = trans.get_showing()
    movie = showing.get_movie()
    tickets = getShowingTickets(showing.get_id())
    return render_template("redeem-ticket.html", trans=trans, showing=showing, movie=movie, tickets=tickets)
    



@member_bp.route("/pick-seat/<int:show_id>", methods=["GET", "POST"])
def pickSeat(show_id):
    if "id" not in session:
        return redirect(url_for("logout"))
    showingData = getShowingData(show_id)
    if request.method == "POST":
        if request.form['input-pin-number'] != session["pinNum"]:
            return render_template("pick-seat.html", show_id=show_id, showing_data=showingData, error="Pin Anda Salah")
        if request.form.getlist("selected_items") == []:
            return render_template("pick-seat.html", show_id=show_id, showing_data=showingData, error="Pilih Seat anda")

        if float(request.form['total-price']) > session["wallet"]:
            return render_template("pick-seat.html", show_id=show_id, showing_data=showingData, error="Saldo anda Tidak mencukupi")
        db = mysqlConnector.connect()
        cursor = db.cursor()
        finalBalance = session['wallet'] - int(request.form['total-price']  )
        query = "UPDATE member SET wallet=%s where id=%s"
        cursor.execute(query, (finalBalance, session['id']))
        session["wallet"] = finalBalance
        ticket_seats = request.form.getlist("selected_items")
        db.commit()
        db.close()
        if not buyTicket(session["id"], show_id, ticket_seats):
            return render_template("pick-seat.html", show_id=show_id, showing_data=showingData, picked_seat=getShowingTickets(show_id), error="Gagal membeli Tiket")
        return render_template("confirm-buy.html")
    return render_template("pick-seat.html", show_id=show_id, showing_data=showingData, picked_seat=getShowingTickets(show_id))

@member_bp.route("/movie-showing/<int:movie_id>", methods=["GET", "POST"])
def showMovieShowing(movie_id):
    if "id" not in session:
        return redirect(url_for("logout"))
    movie = getMovieData(movie_id)
    genre_list = getMovieGenre(movie_id)
    showing_dates = getMovieShowingDate(movie_id)
    showing_times = []
    db = mysqlConnector.connect()
    cursor = db.cursor()
    query = "SELECT sh.id, sh.movie_id, sh.start_time, st.price_per_seat from showing sh JOIN studio st ON sh.studio_id=st.id WHERE sh.movie_id=%s ORDER BY sh.start_time ASC"
    cursor.execute(query,(movie_id,))
    current_time= datetime.now()
    for data in cursor.fetchall():
        showing_times.append([data[0], data[2], data[3]])
    selected_id = 0 if request.args.get('selected_id', type=int) == None else  request.args.get('selected_id', type=int)
    
    return render_template("showing-movie.html", movie=movie, genre_list=genre_list, showing_dates=showing_dates, showing_times=showing_times, selected_id=selected_id, current_time=current_time)

@member_bp.route("/top-up", methods=["GET", "POST"])
def showTopUpPage():
    if "id" not in session:
        return redirect(url_for("login_route"))
    if request.method == 'POST':
        if request.form['pin-number'] != session["pinNum"]:
            return render_template("top_up_page.html", error="Pin number is wrong")

        try:
            db = mysqlConnector.connect()
            cursor = db.cursor()
            finalBalance = session['wallet'] + int(request.form['amount'].replace(",", ""))
            query = "UPDATE member SET wallet=%s where id=%s"
            cursor.execute(query, (finalBalance, session['id']))
            session["wallet"] = finalBalance
            db.commit()
            return redirect(url_for("account.showUserProfile"))
        except Exception as e:
            print(e)
            db.rollback()
            return render_template("top_up_page.html")
        finally:
            db.close()

    return render_template("top_up_page.html")


@member_bp.route("/")
def showShowingMovies():
    if "id" not in session:
        return redirect(url_for("login_route"))
    accId = session["id"]
    return render_template("home_page.html", movies= getShowingMovies())

@member_bp.route("/tickets")
def showMemberTicketData():
    if "id" not in session:
        return redirect(url_for("login_route"))
    trans:List[TransactionTicket] = getThisUserTransaction()
    time_showings = []
    for tran in trans:
        date_time = tran.get_showing().get_showingTime().split(" ")
        date = date_time[0].split("-")
        time = date_time[1].split(":")
        time_showings.append([date,time])
    return render_template("tickets_page.html", trans= trans, time_showings=time_showings)

@member_bp.route("/food-beverage")
def showMemberFoodBeverageData():
    if "id" not in session:
        return redirect(url_for("login_route"))
    accId = session["id"]
    return render_template("food_beverage_page.html")

def getTransactionTickets(trans_id:int):
    try:
        db = mysqlConnector.connect()
        tickets:List[Ticket] = []
        cursor = db.cursor()
        query = """
            SELECT t.seat_name from ticket t
            where t.trans_id=%s
        """
        cursor.execute(query, (trans_id,))
        for data in cursor.fetchall():
            tickets.append(Ticket(0, data[0]))
        return tickets
    except Exception as e:
        print("==========================")
        print(e)
        print("==========================")
        db.rollback()
        return []
    finally:
        db.close()

def getSingleTransaction(trans_id:int):
    try:
        db = mysqlConnector.connect()
        transactionTransactionTicket = None
        cursor = db.cursor()
        query = """
            SELECT t.id, tt.showing_id, tt.ticket_status from transaction t
            JOIN transaction_ticket tt ON t.id=tt.trans_id
            JOIN showing s ON tt.showing_id=s.id
            WHERE t.id = %s
            ORDER BY t.id DESC;
        """
        cursor.execute(query, (trans_id,))
        data = cursor.fetchone()
        tickets = getTransactionTickets(data[0])
        showing = getShowingData(data[1])
        ticketStatus =  TicketStatus(data[2])
        return TransactionTicket(data[0],tickets,getMemberData(session["id"]), showing, ticketStatus, None)
    except Exception as e:
        print("==========================")
        print(e)
        print("==========================")
        db.rollback()
        return []
    finally:
        db.close()

def redeemSingleTransaction(trans_id:int):
    if "id" not in session:
        return redirect(url_for("login_route"))
    try:
        db = mysqlConnector.connect()
        cursor = db.cursor()
        query = "UPDATE transaction_ticket tt SET tt.ticket_status=1 where tt.trans_id=%s"
        cursor.execute(query, (trans_id,))
        db.commit()
        return True
    except :
        db.rollback()
        return False
    finally:
        db.close()

def getThisUserTransaction():
    try:
        db = mysqlConnector.connect()
        transactions:List[TransactionTicket]= []
        cursor = db.cursor()
        query = """
            SELECT t.id, tt.showing_id, tt.ticket_status from transaction t
            JOIN transaction_ticket tt ON t.id=tt.trans_id
            JOIN showing s ON tt.showing_id=s.id
            WHERE t.member_id = %s
            ORDER BY t.id DESC;
        """
        cursor.execute(query, (session["id"],))
        for data in cursor.fetchall():
            tickets = getTransactionTickets(data[0])
            showing = getShowingData(data[1])
            ticketStatus =  TicketStatus(data[2])
            transactions.append(TransactionTicket(data[0],tickets,getMemberData(session["id"]), showing, ticketStatus, None))
        
        return transactions
    except Exception as e:
        print("==========================")
        print(e)
        print("==========================")
        db.rollback()
        return []
    finally:
        db.close()

def getShowingTickets(show_id:int):
    try:
        db = mysqlConnector.connect()
        cursor = db.cursor()
        tickets = []
        query = """
            select t.seat_name from transaction_ticket tt
            JOIN showing s ON tt.showing_id=s.id
            JOIN ticket t ON t.trans_id=tt.trans_id
            WHERE s.id=%s
        """
        cursor.execute(query, (show_id,))
        for data in cursor.fetchall():
            tickets.append(data[0])
        return tickets
        print("==========================")
        print(e)
        print("==========================")
    except Exception as e:
        db.rollback()
        return []
    finally:
        db.close()

def getMovieShowingDate(movie_id:int):
    try:
        data = []
        db = mysqlConnector.connect()
        cursor = db.cursor()
        query = "SELECT DISTINCT DATE(start_time) as idk FROM showing WHERE movie_id=%s and start_time > NOW() ORDER BY DATE(start_time)"
        cursor.execute(query, (movie_id,))
        for dt in cursor.fetchall():
            data.append(dt[0])
        return data
    except Exception as e:
        print("==========================")
        print(e)
        print("==========================")
        db.rollback()
        return []
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
        print("==========================")
        print(e)
        print("==========================")
        return []
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
        print("==========================")
        print(e)
        print("==========================")
        db.rollback()
        return None
    finally:
        db.close()

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

def publishReviewFor(id_review:int, score:int, review:str):
    try:
        db = mysqlConnector.connect()
        cursor = db.cursor()
        query = "UPDATE review_film SET score=%s, review=%s WHERE id=%s"
        cursor.execute(query, (score, review, id_review))
        db.commit()
        return True
    except Exception as e:
        print(e)
        db.rollback()
        return False
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
        query = "SELECT a.id, a.name, a.email, a.password, a.pinNum, a.role, m.wallet from account as a RIGHT JOIN member as m ON a.id = m.id WHERE a.id=%s AND a.role=%s LIMIT 1"
        cursor.execute(query, (memberId, Role.MEMBER.value))
        data = cursor.fetchone()
        member = Member(int(data[0]), data[1], data[2], data[3],data[4], float(data[6]))
        return member
    except Exception as e:
        print(e)
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
            items.append(accountController.getFoodBeverageData(fbId))
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
