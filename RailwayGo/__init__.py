# init.py

from flask import Flask
from flask_login import LoginManager
from .models import connect_db, get_user_by_email
from .views import views
from .auth import auth

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "testtest"
    app.config['DATABASE'] = '/home/ezatul/TT8L-06/database.db'  

    with app.app_context():
        connect_db()

    app.static_folder = 'static'

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return get_user_by_email(id)

    return app








    