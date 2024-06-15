from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('Ticketing.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    trains = conn.execute('SELECT * FROM trains').fetchall()
    conn.close()
    return render_template('ets.html', trains=trains)

@app.route('/train/<int:train_id>')
def train_details(train_id):
    conn = get_db_connection()
    train = conn.execute('SELECT * FROM trains WHERE id = ?', (train_id,)).fetchone()
    seats = conn.execute('SELECT * FROM seats WHERE train_id = ?', (train_id,)).fetchall()
    conn.close()
    return render_template('komuter.html', train=train, seats=seats)

@app.route('/book', methods=('GET', 'POST'))
def book_seat():
    if request.method == 'POST':
        train_id = request.form['train_id']
        seat_number = request.form['seat_number']
        conn = get_db_connection()
        conn.execute('UPDATE seats SET status = ? WHERE train_id = ? AND seat_number = ?', ('booked', train_id, seat_number))
        conn.commit()
        conn.close()
        return redirect(url_for('train_details', train_id=train_id))
    return render_template('book.html')

if __name__ == '__main__':
    app.run(debug=True)
