import os
import bcrypt
from InquirerPy import inquirer
from InquirerPy.validator import PasswordValidator
from dbconnect import create_connection
from mysql.connector import errors

# login.py

# valid_username = "user123"
# valid_password = "pass123"

def loginmenu():
    print("--------------------------------------------------------------")
    print('        \033[4mWelcome to the Restaurant Management Interface\033[0m')
    print("--------------------------------------------------------------")
    action = inquirer.select(
        message="Select an action:",
        choices=[
            "Login",
            "Signup",
            "Exit",
        ],
        default=None,
    ).execute()
    os.system('cls')

    if action == "Login":
        return login()
    elif action == "Signup":
        return signup()
        

def login():
    # Get username and password
    username = inquirer.text(
        message="Enter Username/Email:",
        validate=lambda text: len(text) > 0,
        invalid_message="Username cannot be empty",
    ).execute()

    password = inquirer.text(
        message="Enter password:",
        validate=lambda text: len(text) >= 8,
        invalid_message="Password must be at least 8 characters long",
    ).execute()

    confirm = inquirer.confirm(message="Confirm?", default=True).execute()

    #creating database connection
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE email = %s;"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            if user is not None:
                #checking hashed password
                if bcrypt.checkpw(password.encode('utf-8'), user[4].encode('utf-8')):
                    print("Login successful")
                    cursor.close()
                    conn.close()
                    return True, username
                else:
                    print("Incorrect password")
                    return False, None
            else:
                print("User not found")
                return False, None
        except errors.ProgrammingError as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

    os.system('cls')
    return False, None

def signup():

    first_name = inquirer.text(
        message="Enter First Name:",
        validate=lambda text: len(text) > 0,
        invalid_message="First Name cannot be empty",
    ).execute()

    last_name = inquirer.text(
        message="Enter Last Name:",
        validate=lambda text: len(text) > 0,
        invalid_message="Last Name cannot be empty",
    ).execute()

    username = inquirer.text(
        message="Enter Username/Email:",
        validate=lambda text: len(text) > 0,
        invalid_message="Username cannot be empty",
    ).execute()

    password = inquirer.text(
        message="Enter password:",
        validate=lambda text: len(text) >= 8,
        invalid_message="Password must be at least 8 characters long",
    ).execute()

    confirm = inquirer.confirm(message="Confirm?", default=True).execute()
    
    # #hashing the password
    hashedpw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    #creating database connection
    conn = create_connection()  
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO users (fname, lname, permission_level, email, password) VALUES ( %s, %s, %s, %s, %s);"
            values = (first_name, last_name, 1, username, hashedpw)
            cursor.execute(query, values)
            conn.commit()
            print("User added successfully")
            cursor.close()
        except errors.ProgrammingError as e:
            print(f"Error: {e}")
        finally:
            conn.close()
    else:
        print("Failed to connect to the database.")
    
    os.system('cls')
    return False, None
    