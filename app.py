from flask import Flask
from main import main

app=Flask(__name__)
app.register_blueprint(main,url_prefix='/main')


if __name__=='__main__':
    app.run(debug=True)
    