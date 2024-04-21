import mysql.connector
from mysql.connector import Error

database_name = 'dbmsproject'
user = 'root'
password = 'ismail'

def create_connection():
    try:
        conn = mysql.connector.connect(host='localhost', password=password, user=user, database=database_name)
        if conn.is_connected():
            print("Connection established to", database_name)
        else:
            print("Connection failed to", database_name)
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None