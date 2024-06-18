import sqlite3

def insert_sample_data():
    conn = sqlite3.connect('train_booking.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Stations (station_name) VALUES ('Station A')")
    cursor.execute("INSERT INTO Stations (station_name) VALUES ('Station B')")
    cursor.execute("INSERT INTO Stations (station_name) VALUES ('Station C')")

    cursor.execute("INSERT INTO Trains (train_name, total_seats) VALUES ('Express Train', 100)")
    cursor.execute("INSERT INTO Trains (train_name, total_seats) VALUES ('Local Train', 200)")

    cursor.execute("INSERT INTO Schedules (train_id, departure_station_id, arrival_station_id, departure_time, arrival_time) VALUES (1, 1, 2, '2024-06-20 08:00', '2024-06-20 12:00')")
    cursor.execute("INSERT INTO Schedules (train_id, departure_station_id, arrival_station_id, departure_time, arrival_time) VALUES (2, 2, 3, '2024-06-20 09:00', '2024-06-20 11:00')")

    cursor.execute("INSERT INTO Seats (schedule_id, seat_class, seat_number) VALUES (1, 'business', 'B1')")
    cursor.execute("INSERT INTO Seats (schedule_id, seat_class, seat_number) VALUES (1, 'economy', 'E1')")
    cursor.execute("INSERT INTO Seats (schedule_id, seat_class, seat_number) VALUES (2, 'business', 'B2')")
    cursor.execute("INSERT INTO Seats (schedule_id, seat_class, seat_number) VALUES (2, 'economy', 'E2')")

    cursor.execute("INSERT INTO Bookings (schedule_id, seat_id, customer_name, booking_time) VALUES (1, 1, 'Alice', '2024-06-15 10:00')")
    cursor.execute("INSERT INTO Bookings (schedule_id, seat_id, customer_name, booking_time) VALUES (2, 3, 'Bob', '2024-06-15 11:00')")

    conn.commit()
    conn.close()
    print("Sample data inserted successfully.")

if __name__ == "__main__":
    insert_sample_data()


