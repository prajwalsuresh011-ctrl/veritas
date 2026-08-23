import sqlite3
from datetime import datetime
import uuid


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

    # Check existing columns
    cursor.execute("PRAGMA table_info(scans)")

    columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    # Add missing columns for old databases
    if "username" not in columns:

        cursor.execute("""
            ALTER TABLE scans
            ADD COLUMN username TEXT
        """)

    if "verification_id" not in columns:

        cursor.execute("""
            ALTER TABLE scans
            ADD COLUMN verification_id TEXT
        """)

        # Give old records verification IDs
        cursor.execute("""
            SELECT id
            FROM scans
            WHERE verification_id IS NULL
        """)

        old_records = cursor.fetchall()

        for row in old_records:

            verification_id = (
                "VERITAS-"
                f"{datetime.now().year}-"
                f"{uuid.uuid4().hex[:8].upper()}"
            )

            cursor.execute("""
                UPDATE scans
                SET verification_id = ?
                WHERE id = ?
            """, (
                verification_id,
                row[0]
            ))

    conn.commit()
    conn.close()


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
            verification_id
        ))

    result = cursor.fetchone()

    conn.close()

    return result


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
