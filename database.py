import sqlite3


DATABASE_NAME = "veritas.db"


# ====================================================
# DATABASE CONNECTION
# ====================================================

def get_connection():

    return sqlite3.connect(DATABASE_NAME)


# ====================================================
# CREATE / UPDATE DATABASE TABLE
# ====================================================

def create_table():

    conn = get_connection()
    cursor = conn.cursor()

    # Create table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            scan_type TEXT,
            target TEXT,
            score INTEGER,
            status TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Check existing columns
    cursor.execute("PRAGMA table_info(scans)")

    columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    # Add username to old database if missing
    if "username" not in columns:

        cursor.execute("""
            ALTER TABLE scans
            ADD COLUMN username TEXT
        """)

    conn.commit()
    conn.close()


# ====================================================
# SAVE SCAN RESULT
# ====================================================

def save_scan(
    username,
    scan_type,
    target,
    score,
    status
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO scans
        (
            username,
            scan_type,
            target,
            score,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        username,
        scan_type,
        target,
        score,
        status
    ))

    conn.commit()
    conn.close()


# ====================================================
# GET USER SCAN HISTORY
# ====================================================

def get_history(username):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            username,
            scan_type,
            target,
            score,
            status,
            date
        FROM scans
        WHERE username = ?
        ORDER BY id DESC
    """, (username,))

    history = cursor.fetchall()

    conn.close()

    return history


# ====================================================
# CLEAR CURRENT USER HISTORY
# ====================================================

def clear_history(username):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM scans
        WHERE username = ?
    """, (username,))

    conn.commit()
    conn.close()


# ====================================================
# GET USER STATISTICS
# ====================================================

def get_statistics(username):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            COUNT(*),

            SUM(
                CASE
                    WHEN status IN (
                        'SAFE',
                        'Verified',
                        'Likely Genuine'
                    )
                    THEN 1
                    ELSE 0
                END
            ),

            SUM(
                CASE
                    WHEN status IN (
                        'SUSPICIOUS',
                        'Needs Review'
                    )
                    THEN 1
                    ELSE 0
                END
            ),

            SUM(
                CASE
                    WHEN status IN (
                        'DANGEROUS',
                        'Suspicious',
                        'FAKE / MANIPULATED IMAGE'
                    )
                    THEN 1
                    ELSE 0
                END
            )

        FROM scans

        WHERE username = ?
    """, (username,))

    result = cursor.fetchone()

    conn.close()

    return {
        "total": result[0] or 0,
        "safe": result[1] or 0,
        "suspicious": result[2] or 0,
        "dangerous": result[3] or 0
    }


# ====================================================
# CREATE DATABASE AUTOMATICALLY
# ====================================================

create_table()