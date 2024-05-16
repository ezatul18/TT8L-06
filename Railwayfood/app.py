from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['DATABASE'] = 'your_database.db'

def get_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                       id INTEGER PRIMARY KEY,
                       name TEXT,
                       description TEXT        
            )
        ''')
        db.commit()


@app.route ("/home")
def home():
    return render_template("home.html")

@app.route ("/store", methods=['GET', 'POST'])
def store():
    if request.method == 'POST':
        query = request.form['query']
        return redirect(url_for('search', query=query))
    return render_template("store.html")

@app.route ("/search")
def search():
    query = request.args.get('query', '')
    if not query:
        return redirect(url_for('store'))
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + query + '%',))
    results = cursor.fetchall()

    return render_template('search_results.html', query=query, results=results)

@app.route ("/cart")
def cart():
    return render_template("cart.html")



if __name__ == "__main__":
    app.run(debug=True)