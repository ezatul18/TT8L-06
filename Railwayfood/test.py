from flask import Flask, render_template, jsonify, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DATABASE_NAME = 'newdatabase.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_database():
    
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    conn.commit()
    conn.close()

@app.route('/store2')
def store2():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()


    products_with_images = []
    for product in products:
        image_path = product[3] 
        product_dict = dict(product)
        product_dict['image_path'] = image_path
        products_with_images.append(product_dict)
        
    return render_template('store2.html', products=products_with_images)

@app.route('/cart')
def cart():
    conn = get_db_connection()
    cart_items = conn.execute('SELECT p.name, p.price, c.quantity FROM products p JOIN cart c ON p.id = c.product_id').fetchall()
    conn.close()
   
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

if __name__ == "__main__":
    create_database()
    app.run(debug = True)
