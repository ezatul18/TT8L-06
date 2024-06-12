from flask import Flask, render_template, jsonify, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/store_food')
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

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])

    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    if product:
        conn.execute('INSERT INTO cart (product_id, quantity) VALUES (?, ?)', (product_id, quantity))
        conn.commit()
        conn.close()
        return redirect(url_for('cart_food'))
    else:
        conn.close()
        return jsonify({'error': 'Product not found'})
    
@app.route('/cart_food')
def cart():
    conn = get_db_connection()
    cart_items = conn.execute('SELECT p.name, p.price, c.quantity FROM products p JOIN cart c ON p.id = c.product_id').fetchall()
    conn.close()
   
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart_food.html', cart_items=cart_items, total_price=total_price)

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
        product_id = request.form['product_id'] 

        conn = get_db_connection()
        conn.execute('DELETE FROM cart WHERE product_id = ?', (product_id,))
        conn.commit()
        conn.close()

        return redirect(url_for('cart_food'))
    
@app.route('/update_delivery', methods=['POST'])
def update_delivery():
    return jsonify({'delivery_charge': 2.00})

@app.route('/update_selfpickup', methods=['POST'])
def update_selfpickup():
    return jsonify({'delivery_charge': 0.00})


if __name__ == "__main__":
    app.run(debug = True)