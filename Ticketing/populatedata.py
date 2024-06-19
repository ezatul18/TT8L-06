import sqlite3

def insert_sample_data():
    conn = sqlite3.connect('train_booking.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Stations (station_name) VALUES ('KUALA LUMPUR')")
    cursor.execute("INSERT INTO Stations (station_name) VALUES ('BATANG MELAKA')")
    cursor.execute("INSERT INTO Stations (station_name) VALUES ('ALOR SETAR')")

    cursor.execute("INSERT INTO Trains (train_name, total_seats) VALUES ('Train1', 100)")
    cursor.execute("INSERT INTO Trains (train_name, total_seats) VALUES ('Train2', 100)")

    cursor.execute("INSERT INTO Schedules (train_id, departure_station_id, arrival_station_id, departure_time, arrival_time) VALUES (1, 1, 2, '2024-06-20 08:00', '2024-06-20 12:00')")
    cursor.execute("INSERT INTO Schedules (train_id, departure_station_id, arrival_station_id, departure_time, arrival_time) VALUES (1, 1, 2, '2024-06-20 14:00', '2024-06-20 18:00')")
    cursor.execute("INSERT INTO Schedules (train_id, departure_station_id, arrival_station_id, departure_time, arrival_time) VALUES (1, 1, 2, '2024-06-20 15:00', '2024-06-20 19:00')")
    cursor.execute("INSERT INTO Schedules (train_id, departure_station_id, arrival_station_id, departure_time, arrival_time) VALUES (1, 2, 3, '2024-06-21 09:00', '2024-06-21 13:00')")
    cursor.execute("INSERT INTO Schedules (train_id, departure_station_id, arrival_station_id, departure_time, arrival_time) VALUES (1, 2, 3, '2024-06-21 11:00', '2024-06-21 15:00')")
    cursor.execute("INSERT INTO Schedules (train_id, departure_station_id, arrival_station_id, departure_time, arrival_time) VALUES (1, 2, 3, '2024-06-21 14:00', '2024-06-21 18:00')")
    cursor.execute("INSERT INTO Schedules (train_id, departure_station_id, arrival_station_id, departure_time, arrival_time) VALUES (1, 3, 2, '2024-06-21 11:00', '2024-06-21 15:00')")
    cursor.execute("INSERT INTO Schedules (train_id, departure_station_id, arrival_station_id, departure_time, arrival_time) VALUES (1, 3, 2, '2024-06-21 16:00', '2024-06-21 20:00')")
    cursor.execute("INSERT INTO Schedules (train_id, departure_station_id, arrival_station_id, departure_time, arrival_time) VALUES (2, 1, 3, '2024-06-22 07:00', '2024-06-22 11:00')")
    cursor.execute("INSERT INTO Schedules (train_id, departure_station_id, arrival_station_id, departure_time, arrival_time) VALUES (2, 1, 3, '2024-06-22 10:00', '2024-06-22 14:00')")
    cursor.execute("INSERT INTO Schedules (train_id, departure_station_id, arrival_station_id, departure_time, arrival_time) VALUES (2, 1, 3, '2024-06-22 13:00', '2024-06-22 17:00')")
    cursor.execute("INSERT INTO Schedules (train_id, departure_station_id, arrival_station_id, departure_time, arrival_time) VALUES (2, 2, 1, '2024-06-23 09:00', '2024-06-23 13:00')")
    cursor.execute("INSERT INTO Schedules (train_id, departure_station_id, arrival_station_id, departure_time, arrival_time) VALUES (2, 2, 1, '2024-06-23 11:00', '2024-06-23 15:00')")
    cursor.execute("INSERT INTO Schedules (train_id, departure_station_id, arrival_station_id, departure_time, arrival_time) VALUES (2, 2, 1, '2024-06-23 15:00', '2024-06-23 19:00')")
    cursor.execute("INSERT INTO Schedules (train_id, departure_station_id, arrival_station_id, departure_time, arrival_time) VALUES (2, 3, 1, '2024-06-21 09:00', '2024-06-21 13:00')")
    cursor.execute("INSERT INTO Schedules (train_id, departure_station_id, arrival_station_id, departure_time, arrival_time) VALUES (2, 3, 1, '2024-06-21 14:00', '2024-06-21 18:00')")

    cursor.execute("INSERT INTO Bookings (schedule_id, seat_id, customer_name, booking_time) VALUES (1, 1, 'Alice', '2024-06-15 10:00')")
    cursor.execute("INSERT INTO Bookings (schedule_id, seat_id, customer_name, booking_time) VALUES (2, 3, 'Bob', '2024-06-15 11:00')")

    for schedule_id in range(1, 6):
         seat_number = 1
         for cubicle in range(1, 5):
            seat_class = 'business' if cubicle <= 2 else 'economy'
            for seat in range(25):  
                seat_number_str = f'{seat_number:02d}'
                cursor.execute("INSERT INTO Seats (schedule_id, seat_number, seat_class, is_available) VALUES (?, ?, ?, ?)",
                               (schedule_id, f'{seat_class[0].upper()}{cubicle}-{seat_number_str}', seat_class, 1))
                seat_number += 1

    conn.commit()
    conn.close()
    print("Sample data inserted successfully.")

if __name__ == "__main__":
    insert_sample_data()


