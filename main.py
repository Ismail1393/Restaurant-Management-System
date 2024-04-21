
import os
from login_file import loginmenu
from dbconnect import create_connection
from employee_view import check_reservations, view_orders, view_menu, insert_order
#from employee_view import employee_view
from mysql.connector import errors  
#from employee_view import check_reservations  # Importing check_reservations function
import bcrypt
from InquirerPy import inquirer
from InquirerPy.validator import PasswordValidator


def main():
    os.system('cls')
    while 1:
        success, user = loginmenu()
        if success:
            while True:
                #creating database connection
                conn = create_connection()
                if conn is not None:
                    try:
                        cursor = conn.cursor()
                        query = "SELECT permission_level FROM users WHERE email = %s;"
                        cursor.execute(query, (user,))
                        permission = cursor.fetchone()
                        if permission[0] == 2:
                            print("Welcome Employee")
                            action = inquirer.select(
                                message="Select an action:",
                                choices=[
                                {"name": "View Reservations", "value": "view_reservations"},
                                {"name": "View Orders", "value": "view_orders"},
                                {"name": "View Menu", "value": "view_menu"},
                                {"name": "Insert New Order", "value": "insert_order"},
                                {"name": "Exit", "value": "exit"},
                            ],
                            default="View Reservations"
                        ).execute()

                        if action == "view_reservations":
                            check_reservations()
                        elif action == "view_orders":
                            view_orders()
                        elif action == "view_menu":
                            view_menu()
                        elif action == "insert_order":
                            insert_order()
                        elif action == "exit":
                            break
                        elif permission[0] == 1:
                            print("Welcome Manager")
                        else:
                            print("Invalid Permission Level")
                            return False

                    except errors.ProgrammingError as e:
                        print(f"Error: {e}")
                    finally:
                        cursor.close()
                        conn.close()
                else:
                    print("Failed to connect to the database.")

if __name__ == "__main__":
    main()
