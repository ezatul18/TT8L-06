from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def booking_page():
    return render_template('ets.html')

@app.route('/get_schedules', methods=['GET'])
def get_schedules():
    conn = sqlite3.connect('train_booking.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT S.schedule_id, T.train_name, S.departure_time, S.arrival_time
        FROM Schedules S
        JOIN Trains T ON S.train_id = T.train_id
    ''')
    schedules = cursor.fetchall()
    conn.close()

    schedules_list = [
        {'schedule_id': schedule[0], 'train_name': schedule[1], 'departure_time': schedule[2], 'arrival_time': schedule[3]}
    for schedule in schedules]
    
    return jsonify({'schedules': schedules_list})

@app.route('/get_seats/<int:schedule_id>', methods=['GET'])
def get_seats(schedule_id):
    conn = sqlite3.connect('train_booking.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT seat_id, seat_class, seat_number 
        FROM Seats 
        WHERE schedule_id = ? AND is_available = 1
    ''', (schedule_id,))
    seats = cursor.fetchall()
    conn.close()

    seats_list = [{'seat_id': seat[0], 'seat_class': seat[1], 'seat_number': seat[2]} for seat in seats]
    
    return jsonify({'seats': seats_list})

@app.route('/book', methods=['POST'])
def book_ticket():
    schedule_id = request.form['schedule']
    seat_id = request.form['seat']
    customer_name = request.form['name']
    booking_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('train_booking.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO Bookings (schedule_id, seat_id, customer_name, booking_time)
        VALUES (?, ?, ?, ?)
    ''', (schedule_id, seat_id, customer_name, booking_time))

    cursor.execute('''
        UPDATE Seats SET is_available = 0 WHERE seat_id = ?
    ''', (seat_id,))
    
    conn.commit()
    conn.close()

    return "Booking successful!"

if __name__ == "__main__":
    app.run(debug=True)

