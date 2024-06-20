

from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from .models import add_user, get_user_by_email, get_user_by_username
from .models import connect_db, add_booking, get_stations
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
auth = Blueprint("auth", __name__)

## LOGIN -SIGNUP ##
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

@auth.route('/book', methods=['GET', 'POST'])
def book_ticket():
    if request.method == 'POST':
        origin = request.form['origin']
        destination = request.form['destination']
        date = request.form['date']
        time = request.form['time']
        num_people = request.form['num_people']
        seat_type = request.form['seat_type']
        seat_number = request.form['seat_number']
        
        db = get_db_connection()
        try:
            # Insert into bookings table
            db.execute('INSERT INTO bookings (origin, destination, date, time, num_people, seat_type, seat_number) VALUES (?, ?, ?, ?, ?, ?, ?)',
                       [origin, destination, date, time, num_people, seat_type, seat_number])
            db.commit()

            # Update seat_status table to mark the seat as booked
            db.execute('UPDATE seat_status SET status = "booked" WHERE seat_number = ?', (seat_number,))
            db.commit()

            flash('Ticket booked successfully!', 'success')
            return redirect(url_for('auth.ticket'))
        except sqlite3.Error as e:
            flash(f'Error booking ticket: {str(e)}', 'error')
        finally:
            db.close()
    
    origins = ['KL', 'Nilai', 'KL Sentral']
    destinations = ['KL', 'Nilai', 'KL Sentral']
    dates = ['2024-08-01', '2024-08-02', '2024-08-03', '2024-08-04', '2024-08-05', '2024-08-06', '2024-08-07', '2024-08-08', '2024-08-09', '2024-08-10', '2024-08-11', '2024-08-12', '2024-08-13', '2024-08-14', '2024-08-15', '2024-08-16', '2024-08-17', '2024-08-18', '2024-08-19', '2024-08-20', '2024-08-21', '2024-08-22', '2024-08-23', '2024-08-24', '2024-08-25', '2024-08-26', '2024-08-27', '2024-08-28', '2024-08-29', '2024-08-30', '2024-08-31']
    times = ['08:00', '16:00', '21:00']
    
    # Fetch seat numbers and availability status from database
    db = get_db_connection()
    cur = db.execute('SELECT seat_number, status FROM seat_status')
    seat_data = cur.fetchall()
    db.close()
    
    # Prepare seat_numbers list based on fetched data
    seat_numbers = [{'number': seat['seat_number'], 'available': seat['status'] == 'available'} for seat in seat_data]

    return render_template('book.html', origins=origins, destinations=destinations, dates=dates, times=times, seat_numbers=seat_numbers)


  



@auth.route('/ticket')
def ticket():
    db = get_db_connection()
    cur = db.execute('SELECT * FROM bookings')
    bookings = cur.fetchall()
    db.close()

    return render_template('ticket.html', bookings=bookings)
