from flask import Flask, request, render_template, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('train_booking.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('book.html')

@app.route('/get_stations')
def get_stations():
    conn = get_db_connection()
    stations = conn.execute('SELECT * FROM Stations').fetchall()
    conn.close()
    return jsonify({'stations': [dict(row) for row in stations]})

@app.route('/get_schedules')
def get_schedules():
    departure_station_id = request.args.get('departure_station_id')
    arrival_station_id = request.args.get('arrival_station_id')
    date = request.args.get('date')
    conn = get_db_connection()
    schedules = conn.execute('''
        SELECT s.schedule_id, t.train_name, s.departure_time, s.arrival_time 
        FROM Schedules s
        JOIN Trains t ON s.train_id = t.train_id
        WHERE s.departure_station_id = ? AND s.arrival_station_id = ? AND date(s.departure_time) = ?
    ''', (departure_station_id, arrival_station_id, date)).fetchall()
    conn.close()
    return jsonify({'schedules': [dict(row) for row in schedules]})

@app.route('/get_seats/<int:schedule_id>/<string:seat_class>')
def get_seats(schedule_id, seat_class):
    conn = get_db_connection()
    seats = conn.execute('''
        SELECT seat_id, seat_number, seat_class, is_available
        FROM Seats
        WHERE schedule_id = ? AND seat_class = ?
    ''', (schedule_id, seat_class)).fetchall()
    conn.close()
    return jsonify({'seats': [dict(row) for row in seats]})

@app.route('/book_ticket', methods=['POST'])
def book_ticket():
    data = request.get_json()
    schedule_id = data.get('schedule_id')
    seat_id = data.get('seat_id')
    num_passengers = data.get('num_passengers')

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO Bookings (schedule_id, seat_id, num_passengers, booking_date)
        VALUES (?, ?, ?, ?)
    ''', (schedule_id, seat_id, num_passengers, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    cursor.execute('''
        UPDATE Seats
        SET is_available = 0
        WHERE seat_id = ?
    ''', (seat_id,))

    conn.commit()
    booking_id = cursor.lastrowid
    conn.close()

    return jsonify({'status': 'success', 'booking_id': booking_id})

if __name__ == '__main__':
    app.run(debug=True)


