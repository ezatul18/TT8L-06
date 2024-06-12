from flask import Flask
from mylogin import *
from mylogin import create_app
from mylogin.routes import routes
app = create_app()

with app.app_context():
    db.create_all()


app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)