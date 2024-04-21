import os
from login_file import loginmenu
from dbconnect import create_connection
from employee_view import check_reservations, view_orders, view_menu, insert_order
from manager_view import update_item_price, insert_menu_item, delete_menu_item, view_sales, average_order_value  # Ensure manager_view is correctly implemented
from mysql.connector import errors
import bcrypt
from InquirerPy import inquirer
from InquirerPy.validator import PasswordValidator

def clear_screen():
    """Clear the console screen on Windows."""
    os.system('cls')

def main():
    clear_screen()
    while True:
        success, user = loginmenu()
        if success:
            while True:
                # Creating database connection
                conn = create_connection()
                if conn is not None:
                    try:
                        cursor = conn.cursor()
                        query = "SELECT permission_level FROM users WHERE email = %s;"
                        cursor.execute(query, (user,))
                        permission = cursor.fetchone()
                        if permission:
                            if permission[0] == 2:  # Employee
                                print("Welcome Employee")
                                while True:
                                    clear_screen()
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
                                        clear_screen()
                                        check_reservations()
                                    elif action == "view_orders":
                                        clear_screen()
                                        view_orders()
                                    elif action == "view_menu":
                                        clear_screen()
                                        view_menu()
                                    elif action == "insert_order":
                                        clear_screen()
                                        insert_order()
                                    elif action == "exit":
                                        break
                            
                            elif permission[0] == 1:  # Manager
                                while True:
                                    clear_screen()
                                    print("Welcome Manager")
                                    action = inquirer.select(
                                        message="Select an action:",
                                        choices=[
                                            {"name": "Edit Menu", "value": "edit_menu"},
                                            {"name": "View Sales", "value": "view_sales"},
                                            {"name": "Exit", "value": "exit"},
                                        ],
                                        default="Edit Menu"
                                    ).execute()

                                    if action == "edit_menu":
                                        sub_action = inquirer.select(
                                            message="Edit Menu Options:",
                                            choices=[
                                                {"name": "Update Item Price", "value": "update_price"},
                                                {"name": "Insert New Menu Item", "value": "insert_item"},
                                                {"name": "Delete Menu Item", "value": "delete_item"},
                                                {"name": "Back", "value": "back"},
                                            ],
                                            default="Update Item Price"
                                        ).execute()

                                        if sub_action == "update_price":
                                            clear_screen()
                                            update_item_price()
                                        elif sub_action == "insert_item":
                                            clear_screen()
                                            insert_menu_item()
                                        elif sub_action == "delete_item":
                                            clear_screen()
                                            delete_menu_item()
                                        elif sub_action == "back":
                                            continue

                                    elif action == "view_sales":
                                        clear_screen()
                                        sales_action = inquirer.select(
                                            message="View Sales Options:",
                                            choices=[
                                                {"name": "View Sales for Today", "value": "view_today_sales"},
                                                {"name": "Average Order Value Today", "value": "avg_order_value"},
                                                {"name": "Back", "value": "back"},
                                            ],
                                            default="View Sales for Today"
                                        ).execute()

                                        if sales_action == "view_today_sales":
                                            clear_screen()
                                            view_sales()
                                        elif sales_action == "avg_order_value":
                                            clear_screen()
                                            average_order_value()
                                        elif sales_action == "back":
                                            continue

                                    elif action == "exit":
                                        return

                        else:
                            print("User has no permission level assigned")
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
