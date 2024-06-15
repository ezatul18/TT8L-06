
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from .models import add_user, get_user_by_email, get_user_by_username
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

