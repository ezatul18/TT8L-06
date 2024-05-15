from flask import Flask, render_template, request, redirect
import sqlite3


app = Flask(__name__)

items = [
    {    
        'id': '1',
        'name': 'Egg & Meat Sandwhich',
        'price': 14,
        'description': 'farm-fresh eggs, savory meats, creamy avocado, rich cheese, and crisp greens, all between freshly baked bread. A symphony of flavors and textures in every bite.',
           
    },
]

connection = sqlite3.connect ('store.db', check_same_thread=False)
db = connection.cursor()

@app.route ("/home")
def home():
    return render_template("home.html")

@app.route ("/store")
def store():
    return render_template("store.html", items=items)

@app.route ("/cart")
def cart():
    return render_template("cart.html")

@app.route ("/add-to-cart/<int:item_id>", methods=["POST"])
def add_to_cart(item_id):
    return redirect("/cart")




if __name__ == "__main__":
    app.run(debug = True)
