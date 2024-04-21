import os
import bcrypt
from login_file import loginmenu
from dbconnect import create_connection
from employee_view import check_reservations, view_orders, view_menu, insert_order
from manager_view import update_item_price, insert_menu_item, delete_menu_item, view_sales, average_order_value, view_employees, check_performance, toggle_employee, view_inventory, order_more, add_new_item
from mysql.connector import errors
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
            exit_flag = False  # Flag to control the loop
            while not exit_flag:  # Check the flag value
                # Creating database connection
                conn = create_connection()
                if conn is not None:
                    try:
                        cursor = conn.cursor()
                        query = "SELECT permission_level FROM users WHERE email = %s;"
                        cursor.execute(query, (user,))
                        permission = cursor.fetchone()
                        if permission[0] == 2:  # Employee
                            print("Welcome Employee")
                            while True:
                                clear_screen()
                                print("--------------------------------------------------------------")
                                print('                 \033[4mEmployee Interface\033[0m')
                                print("--------------------------------------------------------------")
                                action = inquirer.select(
                                    message="Select an action:",
                                    choices=[
                                        {"name": "View Reservations", "value": "view_reservations"},
                                        {"name": "View Orders", "value": "view_orders"},
                                        {"name": "View Menu", "value": "view_menu"},
                                        {"name": "Place New Order", "value": "insert_order"},
                                        {"name": "Exit", "value": "exit"},
                                    ],
                                    default="View Reservations"
                                ).execute()

                                if action == "view_reservations":
                                    clear_screen()
                                    check_reservations()
                                    input("Press enter to continue")
                                elif action == "view_orders":
                                    clear_screen()
                                    view_orders()
                                    input("Press enter to continue")
                                elif action == "view_menu":
                                    clear_screen()
                                    view_menu()
                                    input("Press enter to continue")
                                elif action == "insert_order":
                                    clear_screen()
                                    # Pass the user's email to get their userID
                                    conn = create_connection()
                                    if conn is not None:
                                        try:
                                            cursor = conn.cursor()
                                            query = "SELECT userID FROM users WHERE email = %s;"
                                            cursor.execute(query, (user,))
                                            employee_id = cursor.fetchone()[0]
                                            insert_order(employee_id)
                                        except errors.ProgrammingError as e:
                                            print(f"Error: {e}")
                                        finally:
                                            cursor.close()
                                            conn.close()
                                elif action == "exit":
                                    print("Existing now")
                                    exit_flag = True 
                                    break  
                        elif permission[0] == 1:  # Manager
                            while True:
                                clear_screen()
                                print("--------------------------------------------------------------")
                                print('                 \033[4mManager Interface\033[0m')
                                print("--------------------------------------------------------------")
                                action = inquirer.select(
                                    message="Select an action:",
                                    choices=[
                                        {"name": "Employees", "value": "employees"},
                                        {"name": "Edit Menu", "value": "edit_menu"},
                                        {"name": "View Sales", "value": "view_sales"},
                                        {"name": "Inventory", "value": "inventory"},
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
                                        break  # Break out of the inner loop
                                elif action == "employees":
                                    clear_screen()
                                    print("--------------------------------------------------------------")
                                    print('                 \033[4mEmployee Information\033[0m')
                                    print("--------------------------------------------------------------")
                                    employees_action = inquirer.select(
                                        message="Select Option:",
                                        choices=[
                                            {"name": "View All Employees", "value": "view_employees"},
                                            {"name": "Edit Employee Information", "value": "toggle_employee"},
                                            {"name": "Check Employee Performance", "value": "check_performance"},
                                            {"name": "Exit", "value": "exit"},
                                        ],
                                        default=None
                                    ).execute()

                                    if employees_action == "view_employees":
                                        view_employees()
                                    elif employees_action == "check_performance":
                                        check_performance()
                                    elif employees_action == "toggle_employee":
                                        toggle_employee()
                                    elif employees_action == "exit":
                                        exit_flag = True  # Set the flag to True
                                        break  # Break out of the inner loop
                                
                                elif action == "view_sales":
                                    while True:
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
                                            break

                                elif action == "inventory":
                                    clear_screen()
                                    inventory_action = inquirer.select(
                                        message="Inventory Options:",
                                        choices=[
                                            {"name": "View Total Number of Items", "value": "view_inventory"},
                                            {"name": "Order More", "value": "order_more"},
                                            {"name": "Add New Menu Item", "value": "add_item"},
                                            {"name": "Back", "value": "back"},
                                        ],
                                        default=None
                                    ).execute()

                                    if inventory_action == "view_inventory":
                                        view_inventory()
                                    elif inventory_action == "order_more":
                                        clear_screen()
                                        order_more() 
                                    elif inventory_action == "add_item":
                                        clear_screen()
                                        add_new_item() 
                                    elif inventory_action == "back":
                                        return

                                elif action == "exit":
                                    exit_flag = True  # Set the flag to True
                                    break  # Break out of the inner loop
                        else:
                            print("User has no permission level assigned -- Please Contact Your Manager")
                            return False

                    except errors.ProgrammingError as e:
                        print(f"Error: {e}")
                    finally:
                        cursor.close()
                        conn.close()
                else:
                    print("Failed to connect to the database.")

            # Check the flag value and exit the outer loop if needed
            if exit_flag:
                break

if __name__ == "__main__":
    main()

