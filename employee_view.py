import os
from InquirerPy import inquirer
from dbconnect import create_connection
from mysql.connector import errors

def check_reservations():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "SELECT ReservationID, Available FROM Reservations;"
            cursor.execute(query)
            reservations = cursor.fetchall()

            for reservation in reservations:
                print("Reservation ID:", reservation[0])
                print("Availability:", "Occupied" if reservation[1] else "Available")
                print("------------------------------------------")

            # Ask employee if they want to edit availability
            edit = inquirer.confirm(message="Do you want to edit availability?", default=False).execute()
            if edit:
                reservation_id = inquirer.text(
                    message="Enter Reservation ID to edit availability:",
                    validate=lambda text: text.isdigit(),
                    invalid_message="Please enter a valid Reservation ID.",
                ).execute()

                availability = inquirer.select(
                    message="Select availability:",
                    choices=[
                        "Available",
                        "Occupied",
                    ],
                    default=None,
                ).execute()

                availability_value = 1 if availability == "Occupied" else 0

                update_query = "UPDATE Reservations SET Available = %s WHERE ReservationID = %s;"
                cursor.execute(update_query, (availability_value, reservation_id))
                conn.commit()

                print("Availability updated successfully.")

        except errors.ProgrammingError as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

    else:
        print("Failed to connect to the database.")

def view_orders():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM Orders;"
            cursor.execute(query)
            orders = cursor.fetchall()

            for order in orders:
                print("Order ID:", order[0])
                print("Order Date:", order[1])
                print("Total Price:", order[2])
                print("Employee ID:", order[3])
                print("Quantity:", order[4])
                print("------------------------------------------")

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

def insert_order(employee_id):
    # Display menu to employee
    view_menu()

    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()

            # Get input for order items
            order_items = []
            while True:
                item_id = input("Enter item ID to add to order (or 'done' to finish): ")
                if item_id.lower() == 'done':
                    break
                else:
                    # Validate item ID and fetch item price
                    query = "SELECT ItemPrice FROM Menu WHERE ItemID = %s;"
                    cursor.execute(query, (item_id,))
                    result = cursor.fetchone()
                    if result:
                        order_items.append(result[0])
                    else:
                        print("Invalid item ID. Please try again.")

                    # Calculate total price based on the prices of items fetched from the menu table
                    total_price = sum(order_items)

                    # Insert order into Orders table with EmployeeID
                    insert_query = "INSERT INTO Orders (OrderDate, TotalPrice, EmployeeID, Quantity) VALUES (CURDATE(), %s, %s, %s);"
                    cursor.execute(insert_query, (total_price, employee_id, len(order_items)))
                    conn.commit()

                    query = "CALL decrement_inventory(%s, %s);"
                    values = (item_id, len(order_items))
                    cursor.execute(query, values)
                    conn.commit()
                    
                    print("Order inserted successfully.")

            # Ask customer to rate the employee out of 5
            rating = inquirer.select(
                message="Rate the employee out of 5:",
                choices=[1, 2, 3, 4, 5],
                default=None,
            ).execute()

            # Insert feedback into CustomerFeedback table
            insert_feedback_query = "INSERT INTO customerFeedback (userID, Rating) VALUES (%s, %s);"
            cursor.execute(insert_feedback_query, (employee_id, rating))
            conn.commit()

            print("Customer feedback inserted successfully.")

        except errors.ProgrammingError as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

    else:
        print("Failed to connect to the database.")
        

