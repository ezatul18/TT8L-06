from flask import Flask, send_file , request

app = Flask(__name__)

@app.route('/')
def index():
    return send_file("C:\\Users\\nurti\\TT8L-06\\FoodOrdering system\\Railwayfood.html")



if __name__ == "__main__":
    app.run(debug = True)
 