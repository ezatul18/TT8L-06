from flask import Blueprint, render_template

views = Blueprint("views", __name__, template_folder='templates')

@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html")

@views.route("/about")  
def about():
    return render_template("about.html")

@views.route("/homefood")  
def homefood():
    return render_template("home_food.html")

@views.route("/ets")  
def ets():
    return render_template("ets.html")

@views.route("/ktm")  
def ktm():
    return render_template("ktm.html")

@views.route("/hotel")  
def hotel():
    return render_template("hotel.html")







