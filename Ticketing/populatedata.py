import sqlite3

def populate_db():
    conn = sqlite3.connect('Ticketing.db')
    cursor = conn.cursor()

    ets_trains_data = [
        ('ETS001', 'Station A', 'Station B', '2024-07-01 10:00:00', '2024-07-01 12:00:00'),
        ('ETS002', 'Station B', 'Station C', '2024-07-01 13:00:00', '2024-07-01 15:00:00')
    ]

    ets_seats_data = [
        (1, 'A1', 'available'),
        (1, 'A2', 'booked'),
        (2, 'B1', 'available'),
        (2, 'B2', 'available')
    ]

    komuter_trains_data = [
        ('Komuter001', 'Station X', 'Station Y', '2024-07-01 09:00:00', '2024-07-01 11:00:00'),
        ('Komuter002', 'Station Y', 'Station Z', '2024-07-01 12:00:00', '2024-07-01 14:00:00')
    ]

    komuter_seats_data = [
        (1, 'C1', 'available'),
        (1, 'C2', 'booked'),
        (2, 'D1', 'available'),
        (2, 'D2', 'available')
    ]

    cursor.executemany('''
        INSERT INTO ets_trains (train_number, departure_station, arrival_station, departure_time, arrival_time)
        VALUES (?, ?, ?, ?, ?)
    ''', ets_trains_data)

    cursor.executemany('''
        INSERT INTO ets_seats (train_id, seat_number, status)
        VALUES (?, ?, ?)
    ''', ets_seats_data)

    cursor.executemany('''
        INSERT INTO komuter_trains (train_number, departure_station, arrival_station, departure_time, arrival_time)
        VALUES (?, ?, ?, ?, ?)
    ''', komuter_trains_data)

    cursor.executemany('''
        INSERT INTO komuter_seats (train_id, seat_number, status)
        VALUES (?, ?, ?)
    ''', komuter_seats_data)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    populate_db()
