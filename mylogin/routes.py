from flask import Blueprint, render_template, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mylogin.models import Product, Cart

routes = Blueprint("routes", __name__)


DB_NAME = "database.db"
engine = create_engine(f'sqlite:///{DB_NAME}')
Session = sessionmaker(bind=engine)
session = Session()

# Define routes
@routes.route('/store2')
def store2():
    products = session.query(Product).all()
    return render_template('store2.html', products=products)

@routes.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])

    product = session.query(Product).filter_by(id=product_id).first()
    if product:
        cart_item = Cart(product_id=product_id, quantity=quantity)
        session.add(cart_item)
        session.commit()
        return jsonify({'message': 'Product added to cart successfully'})
    else:
        return jsonify({'error': 'Product not found'})

@routes.route('/cart')
def cart():
    cart_items = session.query(Product.name, Product.price, Cart.quantity).join(Cart).all()
    total_price = sum(item.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)