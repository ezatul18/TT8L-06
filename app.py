from flask import Flask
from mylogin import create_app
from mylogin.routes import routes

app = create_app()


app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)