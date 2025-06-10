from app import create_app
from flask import render_template
from flask import Flask
import pymysql
from flask import Flask, render_template, session, redirect, url_for, request
from pymysql.cursors import DictCursor


app = create_app()
import os
app.secret_key = os.environ.get('SECRET_KEY', 'default_dev_key')

    # Store DB config in app config
app.config['DB_CONFIG'] = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'hotel_db',
        'cursorclass': DictCursor  # ✅ Change this to DictCursor
       
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Simple hardcoded check (replace later with real user check)
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('view_reservations'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/clerk_dashboard')
def view_reservations():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    connection = pymysql.connect(**app.config['DB_CONFIG'])
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM reservation ORDER BY created_at DESC')
    reservation = cursor.fetchall()
    return render_template('clerk_dashboard.html', reservations=reservation)


@app.route('/checkout_page')
def checkout_page():
    return render_template('checkout_page.html')

@app.route('/manager/reports')
def manager_reports():
    return render_template('manager_reports.html')

@app.route('/travel-companies')
def travel_company():
    return render_template('travel_company.html')

if __name__ == '__main__':
    app.run(debug=True, port=5500)
else:
    application = app  # 👈 THIS enables `flask db` command to detect app
    
from flask import Flask, render_template

app = Flask(__name__)





    
