from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{DB_NAME}'

db = SQLAlchemy(app)

from models import Product, Cart, User

# Insert data into the tables
@app.before_first_request
def create_tables():
    db.create_all()
    products_data = [
        {'name': 'Egg&Slice meat Sandwhich', 'price': 15},
        {'name': 'Wanpaku Sandwhich', 'price': 12},
        {'name': 'Croissant Egg&Meat', 'price': 16},
        {'name': 'Ice cream toast berries', 'price': 11},
        {'name': 'Shrimp alfredo', 'price': 11},
        {'name': 'Rice&Curry prawn', 'price': 17.50},
        {'name': 'Garlic bread bits', 'price': 19},
        {'name': 'Honey BBQ boneless Chicken', 'price': 19},
        {'name': 'Garlic butter Steak&Potatoes skillet', 'price': 20},
        {'name': 'Farfalle with Mushrooms&Caramalized Onions', 'price': 18.50},
        {'name': 'Herby lemon Skewers', 'price': 12},
        {'name': 'Futomaki fat sushi', 'price': 13}
    ]
    for product_data in products_data:
        product = Product(**product_data)
        db.session.add(product)
    db.session.commit()

    # Example of adding data to the cart
    cart_item = Cart(product_id=1, quantity=2)  
    db.session.add(cart_item)
    db.session.commit()

from mylogin import create_app

if __name__ == '__main__':
    app.run(debug=True)
