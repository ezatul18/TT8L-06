import sqlite3

def connect_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users
                   (id INTEGER PRIMARY KEY, 
                    email VARCHAR(150) UNIQUE, 
                    username VARCHAR(150) UNIQUE, 
                    password TEXT, 
                    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    conn.commit()
    conn.close()


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


def add_booking(origin, destination, date, time, pax):
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO bookings (origin, destination, date, time, pax) VALUES (?, ?, ?, ?, ?)',
                     (origin, destination, date, time, pax))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise
    finally:
        conn.close()

def get_stations():
    conn = get_db_connection()
    stations = conn.execute('SELECT name FROM stations').fetchall()
    conn.close()
    return [station['name'] for station in stations]


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn



