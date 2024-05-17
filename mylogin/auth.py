# mylogin/auth.py

from flask import Blueprint, render_template , redirect,url_for, request

auth = Blueprint("auth", __name__)

@auth.route("/login" , methods=['GET','POST'])
def login():
    return render_template("login.html")
    email = request.form.get("email")
    password = request.form.get("password")


@auth.route("/sign-up" , methods=['GET','POST'])
def sign_up():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    return render_template("sign_up.html", methods=['GET','POST'])

@auth.route("/logout")
def logout():
    return redirect(url_for("views.home"))