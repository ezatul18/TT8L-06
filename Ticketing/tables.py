import sqlite3

def create_tables():
    conn = sqlite3.connect('train_booking.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Seats (
            seat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            seat_number TEXT,
            seat_class TEXT,
            is_available INTEGER
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()


