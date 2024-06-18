import sqlite3

def create_tables():
    conn = sqlite3.connect('train_booking.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Stations (
        station_id INTEGER PRIMARY KEY AUTOINCREMENT,
        station_name TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Trains (
        train_id INTEGER PRIMARY KEY AUTOINCREMENT,
        train_name TEXT NOT NULL,
        total_seats INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Schedules (
        schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
        train_id INTEGER,
        departure_station_id INTEGER,
        arrival_station_id INTEGER,
        departure_time TEXT NOT NULL,
        arrival_time TEXT NOT NULL,
        FOREIGN KEY (train_id) REFERENCES Trains(train_id),
        FOREIGN KEY (departure_station_id) REFERENCES Stations(station_id),
        FOREIGN KEY (arrival_station_id) REFERENCES Stations(station_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Seats (
        seat_id INTEGER PRIMARY KEY AUTOINCREMENT,
        schedule_id INTEGER,
        seat_class TEXT NOT NULL CHECK(seat_class IN ('business', 'economy')),
        seat_number TEXT NOT NULL,
        is_available BOOLEAN DEFAULT 1,
        FOREIGN KEY (schedule_id) REFERENCES Schedules(schedule_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Bookings (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        schedule_id INTEGER,
        seat_id INTEGER,
        customer_name TEXT NOT NULL,
        booking_time TEXT NOT NULL,
        FOREIGN KEY (schedule_id) REFERENCES Schedules(schedule_id),
        FOREIGN KEY (seat_id) REFERENCES Seats(seat_id)
    )
    ''')

    conn.commit()
    conn.close()
    print("Tables created successfully.")

if __name__ == "__main__":
    create_tables()
