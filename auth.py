import sqlite3
import hashlib


DATABASE = "users.db"


# =========================================
# Create User Database
# =========================================

def create_user_table():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
        """
    )

    conn.commit()
    conn.close()



# =========================================
# Password Encryption
# =========================================

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()



# =========================================
# Register User
# =========================================

def register_user(username, password):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    try:

        cursor.execute(
            """
            INSERT INTO users
            (username,password)

            VALUES (?,?)
            """,

            (
                username,
                hash_password(password)
            )
        )


        conn.commit()

        return True


    except:

        return False


    finally:

        conn.close()



# =========================================
# Login Verification
# =========================================

def login_user(username,password):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username=? 
        AND password=?
        """,

        (
            username,
            hash_password(password)
        )
    )


    user = cursor.fetchone()


    conn.close()


    return user



create_user_table()