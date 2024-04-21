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
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "SELECT OrderDate, SUM(TotalPrice) FROM Orders WHERE OrderDate = CURDATE() GROUP BY OrderDate;"
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                print(f"Total sales for today ({result[0]}): ${result[1]:.2f}")
            else:
                print("No sales recorded for today.")
        except errors.ProgrammingError as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

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

