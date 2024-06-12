

from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import add_user, get_user_by_email, get_user_by_username
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = get_user_by_email(email)
        if user:
            if check_password_hash(user[3], password):  
                flash('Logged in')
                
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

