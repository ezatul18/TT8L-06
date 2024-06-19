import sqlite3

def insert_sample_data():
    conn = sqlite3.connect('train_booking.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT COUNT(*) 
        FROM Seats 
        WHERE seat_class = 'business'
    ''')
    business_count = cursor.fetchone()[0]

    if business_count < 50:
        for seat_number in range(business_count + 1, min(business_count + 51, 51)):
            seat_number_str = f'{seat_number:02d}'
            cursor.execute("INSERT INTO Seats (seat_number, seat_class, is_available) VALUES (?, ?, ?)",
                           (f'B{seat_number_str}', 'business', 1))

    cursor.execute('''
        SELECT COUNT(*) 
        FROM Seats 
        WHERE seat_class = 'economy'
    ''')
    economy_count = cursor.fetchone()[0]

    if economy_count < 50:
        for seat_number in range(economy_count + 1, min(economy_count + 51, 51)):
            seat_number_str = f'{seat_number:02d}'
            cursor.execute("INSERT INTO Seats (seat_number, seat_class, is_available) VALUES (?, ?, ?)",
                           (f'E{seat_number_str}', 'economy', 1))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    insert_sample_data()




