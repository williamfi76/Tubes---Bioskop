from typing import List

from flask import Blueprint, render_template
from Controller import mysqlConnector
from Controller.accountController import getFoodBeverageData
from Model.foodBeverage import FoodBeverage
from Model.foodBeverageStatus import FoodBeverageStatus
from Model.transactionFoodBeverage import TransactionFoodBeverage

employee_bp = Blueprint('employee', __name__, url_prefix='/employee')

@employee_bp.route("movies/<int:member_id>")
def movie_homepage(member_id):
    return render_template("home_page.html", member_id=member_id)

def getAllFoodBeverageOrdersFromTransaction(trans_id: int):
    items:List[FoodBeverage] = []
    try:
        db = mysqlConnector.connect()
        cursor = db.cursor()
        query = """  
                SELECT o.item from order_food_beverage o WHERE o.trans_id=%s
            """
        cursor.execute(query, (trans_id,))
        for item in cursor.fetchall():
            items.append(getFoodBeverageData(item[0]))
        return items
    except Exception as e:
        print(e)
        return items
    finally:
        db.close()

def getAllFoodBeverageTransaction():
    transactions:List[TransactionFoodBeverage] = []
    try:
        db = mysqlConnector.connect()
        cursor = db.cursor()
        query = """  
            SELECT t.id, t.member_id, t.nominal, tf.status from transaction t
            JOIN transaction_food_beverage tf ON 
            WHERE t.status = 0
            ORDER BY t.trans_id DESC
        """
        cursor.execute(query)
        for data in cursor.fetchall():
            items = getAllFoodBeverageOrdersFromTransaction
            currTransaction:TransactionFoodBeverage = TransactionFoodBeverage(data[0], items ,data[2], FoodBeverageStatus(data[3]), data[1])
            transactions.append(currTransaction)
        return transactions
    except Exception as e:
        print(e)
        return transactions
    finally:
        db.close()