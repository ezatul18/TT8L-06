import sqlite3

def populate_data():
    conn = sqlite3.connect('Ticketing.db')
    c = conn.cursor()

    c.execute('INSERT INTO ets_trains (train_number, departure_station, arrival_station, departure_time, arrival_time) VALUES (?, ?, ?, ?, ?)',
              ('ETS123', 'Station A', 'Station B', '09:00', '12:00'))
    c.execute('INSERT INTO ets_trains (train_number, departure_station, arrival_station, departure_time, arrival_time) VALUES (?, ?, ?, ?, ?)',
              ('ETS456', 'Station C', 'Station D', '14:00', '17:00'))

    c.execute('INSERT INTO komuter_trains (train_number, departure_station, arrival_station, departure_time, arrival_time) VALUES (?, ?, ?, ?, ?)',
              ('KOM123', 'Station E', 'Station F', '07:00', '09:00'))
    c.execute('INSERT INTO komuter_trains (train_number, departure_station, arrival_station, departure_time, arrival_time) VALUES (?, ?, ?, ?, ?)',
              ('KOM456', 'Station G', 'Station H', '15:00', '17:00'))

    for i in range(1, 11):
        c.execute('INSERT INTO ets_seats (train_id, seat_number, status) VALUES (?, ?, ?)', (1, f'A{i}', 'available'))
        c.execute('INSERT INTO ets_seats (train_id, seat_number, status) VALUES (?, ?, ?)', (2, f'B{i}', 'available'))

    for i in range(1, 11):
        c.execute('INSERT INTO komuter_seats (train_id, seat_number, status) VALUES (?, ?, ?)', (1, f'C{i}', 'available'))
        c.execute('INSERT INTO komuter_seats (train_id, seat_number, status) VALUES (?, ?, ?)', (2, f'D{i}', 'available'))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    populate_data()

