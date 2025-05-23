from Model.foodBeverage import FoodBeverage
from Model.foodBeverageType import FoodBeverageType
from Model.role import Role
from Controller import mysqlConnector


def register(name:str, email:str, password:str, role:Role, pinNum:str):
    try:
        if email_exists(email):
            return False
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
        
        return result is not None
    except Exception as e:
        return False

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

