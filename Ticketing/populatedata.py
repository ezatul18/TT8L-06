import sqlite3

def insert_sample_data():
    conn = sqlite3.connect('train_booking.db')
    cursor = conn.cursor()

    for schedule_id in range(1, 6):
        for cubicle in range(1, 5):  
            seat_class = 'business' if cubicle <= 2 else 'economy'
            for seat_number in range(1, 51):  
                seat_number_str = f'{seat_number:02d}'
                cursor.execute("INSERT INTO Seats (seat_number, seat_class, is_available) VALUES (?, ?, ?)",
                               (f'{seat_class[0].upper()}{cubicle}-{seat_number_str}', seat_class, 1))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    insert_sample_data()



