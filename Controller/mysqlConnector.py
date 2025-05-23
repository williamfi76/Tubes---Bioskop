import mysql.connector as mp

def connect():
    db = mp.connect(
        host="localhost", 
        user="root", 
        passwd="1234", 
        database="tubes_rpll"
    )
    return db