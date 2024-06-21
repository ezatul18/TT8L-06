import sqlite3

def connect_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Create users table
    cur.execute('''CREATE TABLE IF NOT EXISTS users
                   (id INTEGER PRIMARY KEY, 
                    email VARCHAR(150) UNIQUE, 
                    username VARCHAR(150) UNIQUE, 
                    password TEXT, 
                    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    # Create seat_status table
    cur.execute('''CREATE TABLE IF NOT EXISTS seat_status
                   (seat_number INTEGER PRIMARY KEY,
                    status TEXT NOT NULL)''')

    # Create ets_seat_status table
    cur.execute('''CREATE TABLE IF NOT EXISTS ets_seat_status
                   (seat_number INTEGER PRIMARY KEY,
                    status TEXT NOT NULL)''')

    # Create products table
    cur.execute('''CREATE TABLE IF NOT EXISTS products
                   (id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    price REAL NOT NULL)''')

    conn.commit()
    conn.close()

# Other functions
def add_user(email, username, password):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)", (email, username, password))
    conn.commit()
    conn.close()

def get_user_by_email(email):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cur.fetchone()
    conn.close()
    return user

def get_user_by_username(username):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cur.fetchone()
    conn.close()
    return user

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn





