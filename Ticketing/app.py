from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def booking_page():
    return render_template('ets.html')

@app.route('/get_stations', methods=['GET'])
def get_stations():
    conn = sqlite3.connect('train_booking.db')
    cursor = conn.cursor()
    cursor.execute('SELECT station_id, station_name FROM Stations')
    stations = cursor.fetchall()
    conn.close()

    stations_list = [{'station_id': station[0], 'station_name': station[1]} for station in stations]
    
    return jsonify({'stations': stations_list})

@app.route('/get_schedules', methods=['GET'])
def get_schedules():
    departure_station_id = request.args.get('departure_station_id')
    arrival_station_id = request.args.get('arrival_station_id')
    conn = sqlite3.connect('train_booking.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.schedule_id, t.train_name, s.departure_time, s.arrival_time
        FROM Schedules s
        JOIN Trains t ON s.train_id = t.train_id
        WHERE s.departure_station_id = ? AND s.arrival_station_id = ?
    ''', (departure_station_id, arrival_station_id))
    schedules = cursor.fetchall()
    conn.close()

    schedules_list = [{'schedule_id': sched[0], 'train_name': sched[1], 'departure_time': sched[2], 'arrival_time': sched[3]} for sched in schedules]

    return jsonify({'schedules': schedules_list})

@app.route('/get_seats/<int:schedule_id>/<string:seat_class>', methods=['GET'])
def get_seats(schedule_id, seat_class):
    conn = sqlite3.connect('train_booking.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT seat_id, seat_number, is_available 
        FROM Seats 
        WHERE schedule_id = ? AND seat_class = ?
    ''', (schedule_id, seat_class))
    seats = cursor.fetchall()
    conn.close()

    seats_list = [{'seat_id': seat[0], 'seat_number': seat[1], 'is_available': seat[2]} for seat in seats]

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

