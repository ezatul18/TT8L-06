from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('Ticketing.db')
    conn.row_factory = sqlite3.Row  
    return conn

@app.route('/ets')
def ets_trains():
    conn = get_db_connection()
    ets_trains = conn.execute('SELECT * FROM ets_trains').fetchall()
    conn.close()
    return render_template('ets.html', trains=ets_trains)

@app.route('/ets/train/<int:train_id>')
def ets_train_details(train_id):
    conn = get_db_connection()
    train = conn.execute('SELECT * FROM ets_trains WHERE id = ?', (train_id,)).fetchone()
    seats = conn.execute('SELECT * FROM ets_seats WHERE train_id = ?', (train_id,)).fetchall()
    conn.close()
    return render_template('book.html', train=train, seats=seats, book_url='ets_book_seat')

@app.route('/ets/book', methods=('GET', 'POST'))
def ets_book_seat():
    if request.method == 'POST':
        train_id = request.form['train_id']
        seat_number = request.form['seat_number']
        conn = get_db_connection()
        conn.execute('UPDATE ets_seats SET status = ? WHERE train_id = ? AND seat_number = ?', ('booked', train_id, seat_number))
        conn.commit()
        conn.close()
        return redirect(url_for('ets_train_details', train_id=train_id))

@app.route('/komuter')
def komuter_trains():
    conn = get_db_connection()
    komuter_trains = conn.execute('SELECT * FROM komuter_trains').fetchall()
    conn.close()
    return render_template('komuter.html', trains=komuter_trains)

@app.route('/komuter/train/<int:train_id>')
def komuter_train_details(train_id):
    conn = get_db_connection()
    train = conn.execute('SELECT * FROM komuter_trains WHERE id = ?', (train_id,)).fetchone()
    seats = conn.execute('SELECT * FROM komuter_seats WHERE train_id = ?', (train_id,)).fetchall()
    conn.close()
    return render_template('book.html', train=train, seats=seats, book_url='komuter_book_seat')

@app.route('/komuter/book', methods=('GET', 'POST'))
def komuter_book_seat():
    if request.method == 'POST':
        train_id = request.form['train_id']
        seat_number = request.form['seat_number']
        conn = get_db_connection()
        conn.execute('UPDATE komuter_seats SET status = ? WHERE train_id = ? AND seat_number = ?', ('booked', train_id, seat_number))
        conn.commit()
        conn.close()
        return redirect(url_for('komuter_train_details', train_id=train_id))

if __name__ == '__main__':
    app.run(debug=True)
