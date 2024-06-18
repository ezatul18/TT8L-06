import sqlite3

def insert_sample_data():
    conn = sqlite3.connect('train_booking.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Stations (station_name) VALUES ('KUALA LUMPUR')")
    cursor.execute("INSERT INTO Stations (station_name) VALUES ('BATANG MELAKA')")
    cursor.execute("INSERT INTO Stations (station_name) VALUES ('ALOR SETAR')")

    cursor.execute("INSERT INTO Trains (train_name, total_seats) VALUES ('Train1', 100)")
    cursor.execute("INSERT INTO Trains (train_name, total_seats) VALUES ('Train2', 100)")

    cursor.execute('''
        INSERT INTO Schedules (train_id, departure_station_id, arrival_station_id, departure_time, arrival_time)
        VALUES (1, 1, 2, '2024-06-20 08:00', '2024-06-20 12:00')
    ''')
    cursor.execute('''
        INSERT INTO Schedules (train_id, departure_station_id, arrival_station_id, departure_time, arrival_time)
        VALUES (2, 2, 3, '2024-06-20 09:00', '2024-06-20 11:00')
    ''')

    cursor.execute("INSERT INTO Seats (schedule_id, seat_class, seat_number, is_available) VALUES (1, 'business', 'B1', 1)")
    cursor.execute("INSERT INTO Seats (schedule_id, seat_class, seat_number, is_available) VALUES (1, 'economy', 'E1', 1)")
    cursor.execute("INSERT INTO Seats (schedule_id, seat_class, seat_number, is_available) VALUES (2, 'business', 'B2', 1)")
    cursor.execute("INSERT INTO Seats (schedule_id, seat_class, seat_number, is_available) VALUES (2, 'economy', 'E2', 1)")

    cursor.execute("INSERT INTO Bookings (schedule_id, seat_id, customer_name, booking_time) VALUES (1, 1, 'Alice', '2024-06-15 10:00')")
    cursor.execute("INSERT INTO Bookings (schedule_id, seat_id, customer_name, booking_time) VALUES (2, 3, 'Bob', '2024-06-15 11:00')")

    conn.commit()
    conn.close()
    print("Sample data inserted successfully.")

if __name__ == "__main__":
    insert_sample_data()


