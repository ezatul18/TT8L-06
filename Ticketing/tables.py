import sqlite3

def init_db():
    conn = sqlite3.connect('Ticketing.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ets_trains (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            train_number TEXT NOT NULL,
            departure_station TEXT NOT NULL,
            arrival_station TEXT NOT NULL,
            departure_time TEXT NOT NULL,
            arrival_time TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ets_seats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            train_id INTEGER,
            seat_number TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY(train_id) REFERENCES ets_trains(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS komuter_trains (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            train_number TEXT NOT NULL,
            departure_station TEXT NOT NULL,
            arrival_station TEXT NOT NULL,
            departure_time TEXT NOT NULL,
            arrival_time TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS komuter_seats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            train_id INTEGER,
            seat_number TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY(train_id) REFERENCES komuter_trains(id)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
