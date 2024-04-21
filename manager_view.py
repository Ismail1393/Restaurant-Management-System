# manager_view.py

import os
from InquirerPy import inquirer
from dbconnect import create_connection
from mysql.connector import errors

def update_item_price():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            view_menu()  # Assuming view_menu function is imported or defined in this module
            item_id = inquirer.text(message="Enter Item ID to update price:").execute()
            new_price = inquirer.text(message="Enter new price:").execute()
            
            update_query = "UPDATE Menu SET ItemPrice = %s WHERE ItemID = %s;"
            cursor.execute(update_query, (new_price, item_id))
            conn.commit()
            print("Item price updated successfully.")
        except errors.ProgrammingError as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def insert_menu_item():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            item_name = inquirer.text(message="Enter Item Name:").execute()
            item_description = inquirer.text(message="Enter Item Description:").execute()
            item_price = inquirer.text(message="Enter Item Price:").execute()
            available = inquirer.confirm(message="Is the item available?", default=True).execute()
            
            insert_query = "INSERT INTO Menu (ItemName, ItemDescription, ItemPrice, Available) VALUES (%s, %s, %s, %s);"
            cursor.execute(insert_query, (item_name, item_description, item_price, available))
            conn.commit()
            print("New menu item added successfully.")
        except errors.ProgrammingError as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def delete_menu_item():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            view_menu()  # Assuming view_menu function is imported or defined in this module
            item_id = inquirer.text(message="Enter Item ID to delete:").execute()
            
            delete_query = "DELETE FROM Menu WHERE ItemID = %s;"
            cursor.execute(delete_query, (item_id,))
            conn.commit()
            print("Menu item deleted successfully.")
        except errors.ProgrammingError as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def view_menu():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM Menu;"
            cursor.execute(query)
            menu_items = cursor.fetchall()

            for item in menu_items:
                print("Item ID:", item[0])
                print("Item Name:", item[1])
                print("Description:", item[2])
                print("Price:", item[3])
                print("Available:", "Yes" if item[4] else "No")
                print("------------------------------------------")

        except errors.ProgrammingError as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def view_sales():
    while True:
        conn = create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                query = "SELECT OrderDate, SUM(TotalPrice) FROM Orders WHERE OrderDate = CURDATE() GROUP BY OrderDate;"
                cursor.execute(query)
                results = cursor.fetchall()
                if results:
                    for result in results:
                        print(f"Total sales for {result[0]}: ${result[1]:.2f}")
                else:
                    print("No sales recorded for today.")
            except errors.ProgrammingError as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            print("Failed to connect to the database.")

        action = inquirer.select(
            message="Select an action:",
            choices=[
                {"name": "Exit", "value": "exit"},
            ],
            default="Exit"
        ).execute()

        if action == "exit":
            break

def average_order_value():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "SELECT AVG(TotalPrice) FROM Orders WHERE OrderDate = CURDATE();"
            cursor.execute(query)
            result = cursor.fetchone()
            if result[0] is not None:
                print(f"Average order value for today: ${result[0]:.2f}")
            else:
                print("No orders have been placed today.")
        except errors.ProgrammingError as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def view_employees():
    while True:
        conn = create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                query = "SELECT * FROM users WHERE permission_level = 2;"
                cursor.execute(query)
                employees = cursor.fetchall()
                for employee in employees:
                    print("Employee ID:", employee[0])
                    print("Name:", employee[1], employee[2])
                    print("Email:", employee[3])
                    print("Permission Level:", employee[6])
                    print("------------------------------------------")

            except errors.ProgrammingError as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            print("Failed to connect to the database.")
        
        action = inquirer.select(
            message="Select an action:",
            choices=[
                {"name": "Exit", "value": "exit"},
            ],
            default="Exit"
        ).execute()

        if action == "exit":
            break

def check_performance():
    os.system("cls")
    while True:
        conn = create_connection()
        if conn is not None:
            try:

                action = inquirer.select(
                    message="Select an action:",
                    choices=[
                        {"name": "View All Employee Sales", "value": "view_sales"},
                        {"name": "View employee performance", "value": "employee_performance"},
                        {"name": "Exit", "value": "exit"},
                    ],
                    default="Exit"
                ).execute()

                if action == "exit":
                    break

                elif action == "view_sales":
                    os.system("cls")
                    cursor = conn.cursor()
                    query = "SELECT u.fname , u.lname, o.EmployeeID, SUM(o.TotalPrice) FROM Orders o INNER JOIN Users u ON o.EmployeeID = u.userID GROUP BY o.EmployeeID;"
                    cursor.execute(query)
                    result = cursor.fetchall()
                    if result:
                        for employee in result:
                            print(f"Employee ID: {employee[0]}")
                            print(f"First Name: {employee[1]}")
                            print(f"Last Name: {employee[2]}")
                            print(f"Total sales: ${employee[3]:.2f}")
                            print("------------------------------------------")
                    else:
                        print("No sales recorded.")
                        
                elif action == "employee_performance":
                    os.system("cls")
                    cursor = conn.cursor()
                    employee_id = inquirer.text(message="Enter Employee ID:").execute()

                    query = "SELECT u.fname, u.lname, SUM(o.TotalPrice) FROM Orders o INNER JOIN Users u ON o.EmployeeID = u.userID WHERE o.EmployeeID = %s;"
                    cursor.execute(query, (employee_id,))
                    result = cursor.fetchone()
                    if result[0] is not None:
                        print(f"First Name: {result[0]}")
                        print(f"Last Name: {result[1]}")
                        print(f"Total sales for today: ${result[2]} ")
                    else:
                        print(f"No sales recorded for {employee_id}.")

            except errors.ProgrammingError as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            print("Failed to connect to the database.")
        

def toggle_employee():
    os.system("cls")
    while True:
        conn = create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                
                query = "SELECT * FROM users;"
                cursor.execute(query)
                employees = cursor.fetchall()
                for employee in employees:
                    print("Employee ID:", employee[0])
                    print("Name:", employee[1], employee[2])
                    print("Email:", employee[3])
                    print("Permission Level:", employee[6])
                    print("------------------------------------------")

                action = inquirer.select(
                    message="Select an action:",
                    choices=[
                        
                        {"name": "Update Employee Information", "value": "update_employee"},
                        {"name": "Exit", "value": "exit"}
                    ],
                    default="Exit"
                ).execute()

                if action == "exit":
                    break
                elif action == "update_employee":
                    employee_id = inquirer.text(message="Enter Employee ID to update:").execute()
                    query = "SELECT * FROM users WHERE UserID = %s;"
                    cursor.execute(query, (employee_id,))
                    Information = cursor.fetchall()
                    os.system("cls")
                    print("Employee ID:", Information[0][0])
                    print("Name:", Information[0][1], Information[0][2])
                    print("Email:", Information[0][3])
                    print("Permission Level:", Information[0][6])
                    print("------------------------------------------")

                    new_fname = inquirer.text(message="Enter new name:").execute()
                    new_lname = inquirer.text(message="Enter new name:").execute()
                    new_email = inquirer.text(message="Enter new email:").execute()
                    new_permission = inquirer.select(
                        message="Select new permission level:",
                        choices=[
                            {"name": "Employee", "value": 2},
                            {"name": "Manager", "value": 1},
                        ]
                    ).execute()

                    update_query = "UPDATE users SET fname = %s,lname = %s, email = %s, permission_level = %s WHERE UserID = %s;"
                    cursor.execute(update_query, (new_fname, new_lname,  new_email, new_permission, employee_id))
                    conn.commit()
                    print("Employee information updated successfully.")


            except errors.ProgrammingError as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            print("Failed to connect to the database.")
    
        

def view_inventory():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "SELECT ItemName, Quantity FROM Inventory;"
            cursor.execute(query)
            inventory_items = cursor.fetchall()
            #clear_screen()
            print("Inventory List:\n")
            for item in inventory_items:
                print(f"Item Name: {item[0]}, Quantity: {item[1]}")
            print("\nEnd of Inventory List")
        except errors.ProgrammingError as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to the database.")


def order_more():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            # Display the current inventory to the manager
            view_inventory()
            
            # Ask for the item name
            item_name = inquirer.text(
                message="Enter the name of the item to order more:"
            ).execute()

            # Ask for the quantity to add
            additional_quantity = inquirer.text(
                message="How many more units do you want to add?",
                validate=lambda text: text.isdigit(),
                invalid_message="Please enter a valid number."
            ).execute()

            # Update the inventory
            update_query = "UPDATE Inventory SET Quantity = Quantity + %s WHERE ItemName = %s;"
            cursor.execute(update_query, (additional_quantity, item_name))
            conn.commit()
            print(f"Inventory updated. Added {additional_quantity} more units to {item_name}.")

        except errors.ProgrammingError as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

