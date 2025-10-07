# auth_module.py
import sqlite3
import bcrypt

# Create database and table
def create_db():
    conn = sqlite3.connect("auth.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password BLOB
                )''')
    conn.commit()
    conn.close()

# Register new user
def register_user(username, password):
    conn = sqlite3.connect("auth.db")
    c = conn.cursor()
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        c.execute("INSERT INTO users VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
    except sqlite3.IntegrityError:
        print("❌ Username already exists.")
    conn.close()

# Verify login
def verify_user(username, password):
    conn = sqlite3.connect("auth.db")
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if row:
        stored_pw = row[0]
        return bcrypt.checkpw(password.encode(), stored_pw)
    return False
