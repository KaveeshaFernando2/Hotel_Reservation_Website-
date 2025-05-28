from app import create_app
from flask import render_template
from flask import Flask
import pymysql

app = create_app()
    # Store DB config in app config
app.config['DB_CONFIG'] = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'hotel_db',
        'cursorclass': pymysql.cursors.Cursor
}



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/reserve')
def reserve():
    return render_template('reservation_form.html')

@app.route('/clerk_dashboard')
def clerk_dashboard():
    return render_template('clerk_dashboard.html')

@app.route('/checkout_page')
def checkout_page():
    return render_template('checkout_page.html')

if __name__ == '__main__':
    app.run(debug=True, port=5500)
else:
    application = app  # 👈 THIS enables `flask db` command to detect app
    
from flask import Flask, render_template

app = Flask(__name__)





    
