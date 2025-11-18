#File handling databases and creating tables
import sqlite3
import os

DB_PATH = os.path.join("data", "users.db")

#Initialise the database
#Create data directories and user table
def initialise_database():
    #Creates directory if it doesn't already exist
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    #Create user table with its fields
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            security_question TEXT NOT NULL,
            security_answer TEXT NOT NULL
        )
    """)

    #Save and close connection
    conn.commit()
    conn.close()

#adds a user to the database if the username is unique, otherwise it rejects the input
def add_user(username, password, security_question, security_answer):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()


        #Insert new user
        cursor.execute("""
            INSERT INTO users (username, passoword, security_question, security_answer)
            VALUES (username, password, security_question, security_answer)
            """, (username, password, security_question, security_answer))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        #This path of code executes if username already exists
        return False
    
def get_user(username):
    #Retrieves user from database depending on the username
    #If successful, should return a dictionary, if not should return None
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, username, password, security_question, security_answer
        FROM users WHERE username = ?
        """, (username,))
    
    result = cursor.fetchone()
    conn.close()

    if result:
        #Convert tuple tp dictionary for easier access
        return{
            "id": result[0],
            "username": result[1],
            "password": result[2],
            "security_question": result[3],
            "security_answer": result[4]
        }
    return None

def updatePassword(username, new_password):
    #update user's password in the database if they change it
    #Should return true if the user is found and false if it isn't
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users SET password = ? WHERE username = ?
    """, (new_password, username))

    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()

    return rows_affected>0

        
