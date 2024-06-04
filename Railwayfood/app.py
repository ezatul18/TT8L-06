from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
              
@app.route ("/home")
def home():
    return render_template("home.html")

@app.route ("/store")
def store():
    return render_template("store.html")

@app.route ("/checkout")
def checkout():
    return render_template("checkout.html")


if __name__ == "__main__":
    app.run(debug=True)