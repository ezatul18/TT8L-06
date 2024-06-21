

from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from functools import wraps
from .models import add_user, get_user_by_email, get_user_by_username
from .models import connect_db, add_booking, get_stations
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
auth = Blueprint("auth", __name__)

## LOGIN -SIGNUP ##

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function




@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = get_user_by_email(email)
        if user:
            if check_password_hash(user[3], password):  
                session['user_id'] = user[0]
                flash('Logged in')
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html")


@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        email_exists = get_user_by_email(email)
        username_exists = get_user_by_username(username)

        if email_exists:
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        elif len(password) < 6:
            flash('Password is too short.', category='error')
        elif len(email) < 4:
            flash('Email is invalid.', category='error')
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            add_user(email, username, hashed_password)
            flash('User created', category='success')
            return redirect(url_for('auth.login'))

    return render_template("sign_up.html")

## LOG OUT ##
@auth.route("/logout")
def logout():
    conn = get_db_connection()
    try:
        conn.execute('''
            UPDATE cart
            SET status = 'deleted'
            WHERE status = 'active'
        ''')
        conn.commit()
    except Exception as e:
       
        print(f"Error updating cart items: {e}")
        conn.rollback()
    finally:
        conn.close()

    session.clear()

    return redirect(url_for('auth.login'))

## ADD TO CART- FOOD ##
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@auth.route ('/storefood')
def store_food():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()


    products_with_images = []
    for product in products:
        image_path = product[3] 
        product_dict = dict(product)
        product_dict['image_path'] = image_path
        products_with_images.append(product_dict)
        
    return render_template('store_food.html', products=products_with_images)

@auth.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])

    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    if product:
        conn.execute('INSERT INTO cart (product_id, quantity) VALUES (?, ?)', (product_id, quantity))
        conn.commit()
        conn.close()
        return redirect(url_for('auth.cart'))
    else:
        conn.close()
        return jsonify({'error': 'Product not found'})
    
@auth.route('/cart')
@login_required
def cart():
    conn = get_db_connection()
    cart_items = conn.execute('''
        SELECT p.id, p.name, p.price, c.quantity
        FROM products p
        JOIN cart c ON p.id = c.product_id
        WHERE c.status = 'active'
    ''').fetchall()

    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    conn.close()
    
    return render_template('cart_food.html', cart_items=cart_items, total_price=total_price)

## REMOVE FROM CART ##
@auth.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = request.form['product_id']

    conn = get_db_connection()
    try:
        conn.execute('UPDATE cart SET status = "deleted" WHERE product_id = ?', (product_id,))
        conn.commit()
        flash('Product removed from cart', category='success')
    except Exception as e:
        flash('Error removing product from cart', category='error')
        conn.rollback()
    finally:
        conn.close()
        return redirect(url_for('auth.cart'))

## DELIVERY METHOD ##
@auth.route('/update_delivery', methods=['POST'])
def update_delivery():
    return jsonify({'delivery_charge': 2.00})

@auth.route('/update_selfpickup', methods=['POST'])
def update_selfpickup():
    return jsonify({'delivery_charge': 0.00})

## SUMMARY PAGE ##
@auth.route('/summary')
def summary():
    conn = get_db_connection()
    
    
    user_id = session.get('user_id') 
    user = conn.execute('SELECT email, username FROM users WHERE id = ?', (user_id,)).fetchone()

    
    cart_items = conn.execute('''
        SELECT p.name, p.price, c.quantity 
        FROM products p 
        JOIN cart c ON p.id = c.product_id 
        WHERE c.status = "active"
    ''').fetchall()

    
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)

    conn.close()

    return render_template('summary.html', user=user, cart_items=cart_items, total_price=total_price)

## BOOK ##

## BOOK KTM ##
@auth.route('/book', methods=['GET', 'POST'])
@login_required

def book_ticket():
    if request.method == 'POST':
        origin = request.form['origin']
        destination = request.form['destination']
        date = request.form['date']
        time = request.form['time']
        num_people = int(request.form['num_people'])
        seat_type = request.form['seat_type']
        seat_numbers = request.form.getlist('seat_number')  

        total_price = calculate_ticket_price(num_people)

        db = get_db_connection()
        try:
            for seat_number in seat_numbers:
                db.execute('INSERT INTO bookings (origin, destination, date, time, num_people, seat_type, seat_number, total_price) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                           [origin, destination, date, time, num_people, seat_type, seat_number, total_price])
                db.execute('UPDATE seat_status SET status = "booked" WHERE seat_number = ?', (seat_number,))
                db.commit()

            flash('Ticket(s) booked successfully!', 'success')
            return redirect(url_for('auth.ticket'))
        except sqlite3.Error as e:
            flash(f'Error booking ticket: {str(e)}', 'error')
        finally:
            db.close()

    origins = ['KL', 'Nilai', 'KL Sentral']
    destinations = ['KL', 'Nilai', 'KL Sentral']
    dates = ['2024-08-01', '2024-08-02', '2024-08-03', '2024-08-04', '2024-08-05', '2024-08-06', '2024-08-07', '2024-08-08', '2024-08-09', '2024-08-10', '2024-08-11', '2024-08-12', '2024-08-13', '2024-08-14', '2024-08-15', '2024-08-16', '2024-08-17', '2024-08-18', '2024-08-19', '2024-08-20', '2024-08-21', '2024-08-22', '2024-08-23', '2024-08-24', '2024-08-25', '2024-08-26', '2024-08-27', '2024-08-28', '2024-08-29', '2024-08-30', '2024-08-31']
    times = ['08:00', '16:00', '21:00']
    
    db = get_db_connection()
    cur = db.execute('SELECT seat_number, status FROM seat_status')
    seat_data = cur.fetchall()
    db.close()
    
    seat_numbers = [{'number': seat['seat_number'], 'available': seat['status'] == 'available'} for seat in seat_data]

    return render_template('book_ktm.html', origins=origins, destinations=destinations, dates=dates, times=times, seat_numbers=seat_numbers)


@auth.route('/ticket')

def ticket():
    conn = get_db_connection()
    cursor = conn.cursor()

    sql_query = """
    SELECT 
        origin, 
        destination, 
        date, 
        time, 
        num_people, 
        seat_type, 
        group_concat(IFNULL(seat_number, ''), ', ') AS seat_numbers, 
        total_price 
    FROM 
        bookings 
    GROUP BY 
        origin, 
        destination, 
        date, 
        time, 
        num_people, 
        seat_type, 
        total_price
    """

    cursor.execute(sql_query)
    rows = cursor.fetchall()

    bookings = []
    for row in rows:
        seat_numbers = row[6].strip(', ')  
        seat_numbers_list = seat_numbers.split(', ') if seat_numbers else []
        total_price = row[7]
        booking = {
            'origin': row[0],
            'destination': row[1],
            'date': row[2],
            'time': row[3],
            'num_people': row[4],
            'seat_type': row[5],
            'seat_numbers': seat_numbers_list,
            'total_price': total_price
        }
        bookings.append(booking)

    conn.close()

    return render_template('ticket_ktm.html', bookings=bookings)





## BOOK ETS ##
from flask import session

@auth.route('/ets_book', methods=['GET', 'POST'])
@login_required
def book_ets_ticket():
    if request.method == 'POST':
        origin = request.form['origin']
        destination = request.form['destination']
        date = request.form['date']
        time = request.form['time']
        num_people = int(request.form['num_people'])
        seat_type = request.form['seat_type']
        seat_numbers = request.form.getlist('seat_number')

        total_price = calculate_ticket_price(num_people)

        db = get_db_connection()
        try:
            for seat_number in seat_numbers:
                db.execute(
                    'INSERT INTO ets_bookings (origin, destination, date, time, num_people, seat_type, seat_number, total_price) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    (origin, destination, date, time, num_people, seat_type, seat_number, total_price)
                )
                db.execute('UPDATE ets_seat_status SET status = "booked" WHERE seat_number = ?', (seat_number,))
            db.commit()

            flash('Ticket(s) booked successfully!', 'success')
            return redirect(url_for('auth.ets_ticket'))
        except sqlite3.Error as e:
            db.rollback()
            flash(f'Error booking ticket: {str(e)}', 'error')
        finally:
            db.close()

    origins = ['Alor Setar', 'Kuala Lumpur', 'Batang Melaka']
    destinations = ['Alor Setar', 'Kuala Lumpur', 'Batang Melaka']
    dates = ['2024-08-01', '2024-08-02', '2024-08-03']
    times = ['08:00', '16:00', '21:00']

    db = get_db_connection()
    cur = db.execute('SELECT seat_number, status FROM ets_seat_status')
    seat_data = cur.fetchall()
    db.close()

    seat_numbers = [{'number': seat['seat_number'], 'available': seat['status'] == 'available'} for seat in seat_data]

    return render_template('book_ets.html', origins=origins, destinations=destinations, dates=dates, times=times, seat_numbers=seat_numbers)

@auth.route('/ets_ticket')
@login_required
def ets_ticket():
    conn = get_db_connection()
    cursor = conn.cursor()

    sql_query = """
    SELECT 
        origin, 
        destination, 
        date, 
        time, 
        num_people, 
        seat_type, 
        group_concat(IFNULL(seat_number, ''), ', ') AS seat_numbers, 
        total_price 
    FROM 
        ets_bookings 
    GROUP BY 
        origin, 
        destination, 
        date, 
        time, 
        num_people, 
        seat_type, 
        total_price
    """

    cursor.execute(sql_query)
    rows = cursor.fetchall()

    ets_bookings = []
    for row in rows:
        seat_numbers = row['seat_numbers'].strip(', ')
        seat_numbers_list = seat_numbers.split(', ') if seat_numbers else []
        total_price = row['total_price']
        booking = {
            'origin': row['origin'],
            'destination': row['destination'],
            'date': row['date'],
            'time': row['time'],
            'num_people': row['num_people'],
            'seat_type': row['seat_type'],
            'seat_numbers': seat_numbers_list,
            'total_price': total_price
        }
        ets_bookings.append(booking)

    conn.close()

def calculate_ticket_price(num_people):
    base_price_per_ticket = 12
    total_price = num_people * base_price_per_ticket
    return total_price




@auth.route('/cancel_ticket/<int:booking_id>', methods=['POST'])

def cancel_ticket(booking_id):
    db = get_db_connection()
    try:
        # Retrieve the booked ticket details
        cur = db.execute('SELECT * FROM ets_bookings WHERE id = ?', (booking_id,))
        booking = cur.fetchone()
        if not booking:
            flash('Booking not found!', 'error')
            return redirect(url_for('auth.ets_ticket'))
        
        # Update seat status to available
        db.execute('UPDATE ets_seat_status SET status = "available" WHERE seat_number = ?', (booking['seat_number'],))
        db.commit()

        # Delete the booking from the database
        db.execute('DELETE FROM ets_bookings WHERE id = ?', (booking_id,))
        db.commit()

        flash('Ticket canceled successfully!', 'success')
    except sqlite3.Error as e:
        flash(f'Error canceling ticket: {str(e)}', 'error')
    finally:
        db.close()
    
    return redirect(url_for('auth.ets_ticket'))