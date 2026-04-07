import sqlite3
import os

DB_PATH = "fraud_detection.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'User'
        )
    ''')
    try:
        c.execute("ALTER TABLE users ADD COLUMN email TEXT")
    except sqlite3.OperationalError:
        pass
    c.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            description TEXT,
            link TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    # Insert default admin if it doesn't exist
    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, email, password, role) VALUES ('admin', 'nehaareddy02@gmail.com', 'admin123', 'Admin')")
        
    conn.commit()
    conn.close()

def add_user(username, email, password, role='User'):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)", (username, email, password, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

def add_report(user_id, report_type, description, link):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO reports (user_id, type, description, link) VALUES (?, ?, ?, ?)", 
              (user_id, report_type, description, link))
    conn.commit()
    conn.close()

def get_all_users():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, username, role FROM users")
    users = c.fetchall()
    conn.close()
    return users

def get_all_reports():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        SELECT reports.id, users.username, reports.type, reports.description, reports.link, reports.timestamp 
        FROM reports 
        JOIN users ON reports.user_id = users.id
        ORDER BY reports.timestamp DESC
    """)
    reports = c.fetchall()
    conn.close()
    return reports

def remove_user(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM reports WHERE user_id=?", (user_id,))
    c.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
