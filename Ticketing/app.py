from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def booking_page():
    return render_template('ets.html')

@app.route('/get_seats/<seat_class>', methods=['GET'])
def get_seats(seat_class):
    conn = sqlite3.connect('train_booking.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT seat_id, seat_number 
        FROM Seats 
        WHERE seat_class = ? AND is_available = 1
    ''', (seat_class,))
    seats = cursor.fetchall()
    conn.close()

    seats_list = [{'seat_id': seat[0], 'seat_number': seat[1]} for seat in seats]
    
    return jsonify({'seats': seats_list})

@app.route('/book', methods=['POST'])
def book_ticket():
    seat_ids = request.form['seat'].split(',')  
    customer_name = request.form['name']
    booking_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('train_booking.db')
    cursor = conn.cursor()

    try:
        for seat_id in seat_ids:
            cursor.execute('''
                INSERT INTO Bookings (seat_id, customer_name, booking_time)
                VALUES (?, ?, ?)
            ''', (seat_id, customer_name, booking_time))

            cursor.execute('''
                UPDATE Seats SET is_available = 0 WHERE seat_id = ?
            ''', (seat_id,))
        
        conn.commit()
        message = "Booking successful!"
    except sqlite3.Error as e:
        conn.rollback()
        message = f"Error booking ticket: {str(e)}"
    finally:
        conn.close()

    return message

if __name__ == "__main__":
    app.run(debug=True)










