import sqlite3

def populate_db():
    conn = sqlite3.connect('Ticketing.db')
    c = conn.cursor()

    trains = [
        ('T101', 'Station A', 'Station B', '2024-07-01 10:00:00', '2024-07-01 12:00:00'),
        ('T102', 'Station B', 'Station C', '2024-07-01 13:00:00', '2024-07-01 15:00:00')
    ]

    seats = [
        (1, 'A1', 'available'),
        (1, 'A2', 'booked'),
        (2, 'B1', 'available'),
        (2, 'B2', 'available')
    ]

    c.executemany('INSERT INTO trains (train_number, departure_station, arrival_station, departure_time, arrival_time) VALUES (?, ?, ?, ?, ?)', trains)
    c.executemany('INSERT INTO seats (train_id, seat_number, status) VALUES (?, ?, ?)', seats)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    populate_db()
