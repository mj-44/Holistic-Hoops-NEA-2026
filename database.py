import sqlite3
import os

DB_PATH = os.path.join("data", "users.db")

#Initialise the database
#Create data directories and user table
def initialise_database():
    #Creates directory if it doesn't already exist
    os.makedirs("data", exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        #Create the user table in the database with its related fields
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                security_question TEXT NOT NULL,
                security_answer TEXT NOT NULL
            )
        """)

        #Create drill scores table and stores every attempt for every drill
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS drill_scores(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                drill_name TEXT NOT NULL,
                makes INTEGER NOT NULL,
                total_shots INTEGER NOT NULL,
                percentage REAL NOT NULL,
                date_completed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        #Create high scores table and stores only the high score for the user and updates when needed
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS high_scores(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                drill_name TEXT NOT NULL,
                makes INTEGER NOT NULL,
                total_shots INTEGER NOT NULL,
                percentage REAL NOT NULL,
                date_achieved TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, drill_name),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        conn.commit()

#adds a user to the database if the username is unique, otherwise it rejects the input
def add_user(username, password, security_question, security_answer):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            params = (username, password, security_question, security_answer)
            cursor.execute("""
                INSERT INTO users
                VALUES (NULL, ?, ?, ?, ?)
                """, params)
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        #This path of code executes if username already exists
        return False
    
def get_user(username):
    #Retrieves user data from the database depending on the user that needs to be searched for
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, password, security_question, security_answer
            FROM users WHERE username = ?
            """, (username,))
        result = cursor.fetchone()

    if result:
        return {
            "id": result[0],
            "username": result[1],
            "password": result[2],
            "security_question": result[3],
            "security_answer": result[4]
        }
    return None

def updatePassword(username, new_password):
    #update user's password in the database if they change it
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users SET password = ? WHERE username = ?
        """, (new_password, username))
        rows_affected = cursor.rowcount
        conn.commit()
    return rows_affected > 0

def save_drill_score(user_id, drill_name, makes, total_shots):
    #Save a completed drill attempt to drill_scores
    #Also update high_scores if this is a new personal best
    percentage = round((makes / total_shots) * 100, 1)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        #Insert the drill score into the drill scores table
        cursor.execute("""
            INSERT INTO drill_scores (user_id, drill_name, makes, total_shots, percentage)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, drill_name, makes, total_shots, percentage))

        #Check if a high score already exists for a user on the certain drill
        cursor.execute("""
            SELECT makes FROM high_scores
            WHERE user_id = ? AND drill_name = ?
        """, (user_id, drill_name))
        existing = cursor.fetchone()

        if existing is None:
            #No existing high score — insert one
            cursor.execute("""
                INSERT INTO high_scores (user_id, drill_name, makes, total_shots, percentage)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, drill_name, makes, total_shots, percentage))
        elif makes > existing[0]:
            #New personal best — update the record
            cursor.execute("""
                UPDATE high_scores
                SET makes = ?, total_shots = ?, percentage = ?, date_achieved = CURRENT_TIMESTAMP
                WHERE user_id = ? AND drill_name = ?
            """, (makes, total_shots, percentage, user_id, drill_name))

        conn.commit()

def get_user_high_scores(user_id):
    #Returns all high scores for a given user as a dictionary keyed by drill name
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT drill_name, makes, total_shots, percentage
            FROM high_scores WHERE user_id = ?
        """, (user_id,))
        results = cursor.fetchall()

    return {
        row[0]: {
            "makes": row[1],
            "total_shots": row[2],
            "percentage": row[3]
        }
        for row in results
    }

def get_high_scores_by_username(username):
    #Returns high scores for a user looked up by username
    user = get_user(username)
    if not user:
        return None
    return get_user_high_scores(user["id"])

def get_all_drill_scores(user_id):
    #Returns the full score history for a given user if needed
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT drill_name, makes, total_shots, percentage, date_completed
            FROM drill_scores WHERE user_id = ?
            ORDER BY date_completed DESC
        """, (user_id,))
        results = cursor.fetchall()

    return [
        {
            "drill_name": row[0],
            "makes": row[1],
            "total_shots": row[2],
            "percentage": row[3],
            "date_completed": row[4]
        }
        for row in results
    ]
