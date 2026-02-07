CONSTANT DB_PATH = join_path("data", "users.db")

FUNCTION initialise_database()
    CREATE_DIRECTORY("data", allow_existing=TRUE)
    
    SET conn TO CONNECT_DATABASE(DB_PATH)
    SET cursor TO conn.cursor()
    
    EXECUTE_SQL(cursor, "
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            security_question TEXT NOT NULL,
            security_answer TEXT NOT NULL
        )
    ")
    
    COMMIT(conn)
    CLOSE(conn)
END FUNCTION


FUNCTION add_user(username, password, security_question, security_answer)
    TRY
        SET conn TO CONNECT_DATABASE(DB_PATH)
        SET cursor TO conn.cursor()
        
        SET params TO (username, password, security_question, security_answer)
        
        EXECUTE_SQL(cursor, "
            INSERT INTO users
            VALUES (NULL, ?, ?, ?, ?)
        ", params)
        
        COMMIT(conn)
        CLOSE(conn)
        RETURN TRUE
        
    CATCH IntegrityError
        RETURN FALSE
    END TRY
END FUNCTION


FUNCTION get_user(username)
    SET conn TO CONNECT_DATABASE(DB_PATH)
    SET cursor TO conn.cursor()
    
    EXECUTE_SQL(cursor, "
        SELECT id, username, password, security_question, security_answer
        FROM users WHERE username = ?
    ", (username))
    
    SET result TO FETCH_ONE_RESULT(cursor)
    CLOSE(conn)
    
    IF result IS NOT NULL THEN
        RETURN dictionary {
            "id": result[0],
            "username": result[1],
            "password": result[2],
            "security_question": result[3],
            "security_answer": result[4]
        }
    END IF
    
    RETURN NULL
END FUNCTION


FUNCTION updatePassword(username, new_password)
    SET conn TO CONNECT_DATABASE(DB_PATH)
    SET cursor TO conn.cursor()
    
    EXECUTE_SQL(cursor, "
        UPDATE users SET password = ? WHERE username = ?
    ", (new_password, username))
    
    SET rows_affected TO GET_ROW_COUNT(cursor)
    COMMIT(conn)
    CLOSE(conn)
    
    RETURN rows_affected > 0
END FUNCTION