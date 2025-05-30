from typing import List
from flask import Blueprint, redirect, render_template, request, session, url_for
from Controller.memberController import getMemberData
from Model.account import Account
from Model.foodBeverage import FoodBeverage
from Model.foodBeverageType import FoodBeverageType
from Model.movie import Movie
from Model.role import Role
from Controller import mysqlConnector
from Model.showing import Showing

account_bp = Blueprint('account', __name__, url_prefix='/account')

@account_bp.route("/profile")
def showUserProfile():
    if "id" not in session:
        return redirect(url_for("login_route"))
    if int(session['role']) == Role.ADMIN.value:
      return render_template("admin_profile_page.html")
    elif int(session['role']) == Role.MEMBER.value:
      return render_template("member_profile_page.html")
    elif int(session['role']) == Role.EMPLOYEE.value:
      return render_template("employee_profile_page.html")

    # return render_template("member_profile_page.html")

@account_bp.route("/update-profile", methods=["GET", "POST"])
def changeProfile():
    if "id" not in session:
        return redirect(url_for("login_route"))
    if request.method == "POST":
        try:
            db = mysqlConnector.connect()
            cursor = db.cursor()
            newName = request.form['new-name']
            query = "UPDATE account SET name=%s where id=%s"
            cursor.execute(query, (newName, session['id']))
            session["name"] = newName
            db.commit()
            return redirect(url_for("account.showUserProfile"))
        except Exception as e:
            print(e)
            db.rollback()
        finally:
            db.close()
    return  render_template("change_username.html")

@account_bp.route("/change-pin-number", methods=["GET", "POST"])
def changePinNumber():
    if "id" not in session:
        return redirect(url_for("login_route"))
    if request.method == "POST":
        try:
            db = mysqlConnector.connect()
            cursor = db.cursor()
            oldPin = request.form['old-pin']
            newPin = request.form['new-pin']
            newPin2 = request.form['new-pin-2']
            if oldPin != session["pinNum"]:
                return render_template("change_password.html", error="Incorrect Pin")
            if newPin2 != newPin:
                return render_template("change_pin_num.html", error="Pins entered are not identical")
            query = "UPDATE account SET pinNum=%s where id=%s"
            cursor.execute(query, (newPin, session["id"]))
            session["pinNum"] = newPin
            db.commit()
            return redirect(url_for("account.showUserProfile"))
        except Exception as e:
            print(e)
            db.rollback()
            return render_template("change_pin_num.html", error="Fail to change Password")

        finally:
            db.close()
    return render_template("change_pin_num.html")

@account_bp.route("/change-password", methods=["GET", "POST"])
def changePassword():
    if "id" not in session:
        return redirect(url_for("login_route"))
    if request.method == "POST":
        try:
            db = mysqlConnector.connect()
            cursor = db.cursor()
            oldPassword = request.form['old-pin-password']
            newPassword = request.form['new-password']
            reenterPassword = request.form['reenter-password']
            if oldPassword != session["password"]:
                return render_template("change_password.html", error="Incorrect Password")
            if newPassword != reenterPassword:
                return render_template("change_password.html", error="Passwords entered are not identical")
            query = "UPDATE account SET password=%s where id=%s"
            cursor.execute(query, (newPassword, session["id"]))
            session["password"] = newPassword
            db.commit()
            return render_template("change_password.html")
        except Exception as e:
            print(e)
            db.rollback()
        finally:
            db.close()
    return render_template("change_password.html")

def show_login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        if not login(email, password):
            return render_template('login.html', error='Email or Password is incorrect')
        account = getAccountData(email)
        session["id"] = account.get_id()
        session["email"] = email
        session["name"] = account.get_name()
        session["role"] = account.get_role().value
        session["password"] = account.get_password()

        if account.role == Role.ADMIN:
            return redirect(url_for("admin.showAdminProfile"))
        elif account.role == Role.EMPLOYEE:
            pass
        elif account.role == Role.MEMBER:
            session["pinNum"] = account.get_pin()
            session["wallet"] = int(getMemberData(account.get_id()).get_wallet())
            return redirect(url_for("member.showShowingMovies"))

    return render_template("login.html")

def show_register():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        pin_num = request.form['pin-num']
        print(name)

        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')
        try:
            if email_exists(email):
                return render_template('register.html', error='Email already exist')
            if not register(name, email, password, Role.MEMBER, pin_num):
                return render_template('register.html', error='Internal Error')
            return redirect(url_for('login_route'))

        except Exception as e:
            return render_template('register.html', error=f"Error: {str(e)}")

    return render_template('register.html')

def register(name:str, email:str, password:str, role:Role, pinNum:str):
    try:
        db = mysqlConnector.connect()
        cursor = db.cursor()

        # Masukkan data account ke tabel account
        cursor.execute("""
            INSERT INTO account (name, email, password, role, pinNum)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, email, password, role.value, pinNum))
        account_id = cursor.lastrowid

        # Apabila role dari account adalah member maka akan dibuat data baru untuk wallet member
        if role == Role.MEMBER:
            cursor.execute("""
                INSERT INTO member (id, wallet)
                VALUES (%s, %s)
            """, (account_id, 0.0))

        db.commit()
        return True
    except Exception as e:
        db.rollback()
        return False

    finally:
        db.close()

def login(email:str, password:str):
    try:
        db = mysqlConnector.connect()
        cursor = db.cursor()

        # Ambil data dari DB dan bandingkan dengan input
        cursor.execute("""
            SELECT id FROM account
            WHERE email = %s AND password = %s
        """, (email, password))
        result = cursor.fetchone()

        account:Account = getAccountData(email)
        
        return result is not None
    except Exception as e:
        db.rollback()
        return False
    finally:
        db.close()

def getAccountData(email:str):
    try:
        db = mysqlConnector.connect()
        cursor = db.cursor()
        query = "SELECT a.id, a.name, a.email, a.password, a.pinNum, a.role from account as a WHERE email=%s LIMIT 1"
        cursor.execute(query, (email,))
        data = cursor.fetchone()
        account = Account(data[0], data[1], data[2], data[3], Role(int(data[5])), data[4])
        return account
    except Exception as e:
        db.rollback()
        return None
    finally:
        db.close()

def email_exists(email_to_check):
    conn = mysqlConnector.connect()
    cursor = conn.cursor()

    query = f"""
        SELECT 1 FROM account WHERE email = %s LIMIT 1
    """
    cursor.execute(query, (email_to_check,))
    result = cursor.fetchone()

    conn.close()
    return result is not None

def getFoodBeverageData(foodBeverageId:int):
    try:
        db = mysqlConnector.connect()
        cursor = db.cursor()
        query = "SELECT fb.id, fb.name, fb.price, fb.type from food_beverage as fb WHERE fb.id=%s"
        cursor.execute(query, (foodBeverageId,))
        data = cursor.fetchone()
        item = FoodBeverage(data[0], data[1], FoodBeverageType(data[3]), data[2])
        return item
    except Exception as e:
        print(e)
        db.rollback()
        return None
    finally:
        db.close()

def logout():
    session.clear()
    return redirect(url_for('login_route'))

