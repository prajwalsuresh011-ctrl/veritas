import sqlite3
from datetime import datetime
import uuid
from pathlib import Path


# ====================================================
# DATABASE PATH
# ====================================================

DATABASE_NAME = Path("veritas.db")


# ====================================================
# DATABASE CONNECTION
# ====================================================

def get_connection():

    return sqlite3.connect(
        str(DATABASE_NAME),
        check_same_thread=False
    )


# ====================================================
# GENERATE VERIFICATION ID
# ====================================================

def generate_verification_id():

    return (
        "VERITAS-"
        f"{datetime.now().year}-"
        f"{uuid.uuid4().hex[:8].upper()}"
    )


# ====================================================
# CREATE / UPDATE DATABASE TABLE
# ====================================================

def create_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            verification_id TEXT UNIQUE,

            username TEXT,

            scan_type TEXT,

            target TEXT,

            score INTEGER,

            status TEXT,

            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
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

    # Make sure database exists
    create_table()

    conn = get_connection()
    cursor = conn.cursor()

    verification_id = generate_verification_id()

    cursor.execute("""
        INSERT INTO scans
        (
            verification_id,
            username,
            scan_type,
            target,
            score,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        verification_id,
        username,
        scan_type,
        target,
        score,
        status
    ))

    conn.commit()
    conn.close()

    return verification_id


# ====================================================
# GET USER SCAN HISTORY
# ====================================================

def get_history(username):

    create_table()

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
            date,
            verification_id
        FROM scans
        WHERE username = ?
        ORDER BY id DESC
    """, (username,))

    history = cursor.fetchall()

    conn.close()

    return history


# ====================================================
# GET SCAN BY VERIFICATION ID
# ====================================================

def get_scan_by_verification_id(
    verification_id,
    username=None
):

    create_table()

    conn = get_connection()
    cursor = conn.cursor()

    if username:

        cursor.execute("""
            SELECT
                id,
                verification_id,
                username,
                scan_type,
                target,
                score,
                status,
                date
            FROM scans
            WHERE verification_id = ?
            AND username = ?
        """, (
            verification_id,
            username
        ))

    else:

        cursor.execute("""
            SELECT
                id,
                verification_id,
                username,
                scan_type,
                target,
                score,
                status,
                date
            FROM scans
            WHERE verification_id = ?
        """, (
            verification_id,
        ))

    result = cursor.fetchone()

    conn.close()

    return result


# ====================================================
# CLEAR CURRENT USER HISTORY
# ====================================================

def clear_history(username):

    create_table()

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

    create_table()

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
# INITIALIZE DATABASE
# ====================================================

create_table()

