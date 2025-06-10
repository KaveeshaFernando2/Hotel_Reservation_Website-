from flask import Blueprint, render_template, request, jsonify, current_app
import pymysql

travel_company_bp = Blueprint('travel_company', __name__)

def get_db():
    db_config = current_app.config['DB_CONFIG']
    return pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        cursorclass=pymysql.cursors.DictCursor
    )

@travel_company_bp.route('/travel-companies')
def view_travel_companies():
    return render_template('travel_company.html')

@travel_company_bp.route('/api/travel-companies', methods=['GET'])
def get_travel_companies():
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM travel_company")
        return jsonify(cursor.fetchall())

@travel_company_bp.route('/api/travel-company', methods=['POST'])
def create_travel_company():
    data = request.json
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO travel_company (company_name, contact_person, email, phone, discount_percentage)
            VALUES (%s, %s, %s, %s, %s)
        """, (data['company_name'], data['contact_person'], data['email'], data['phone'], data['discount_percentage']))
        conn.commit()
    return jsonify({"message": "Travel company created successfully."})

@travel_company_bp.route('/api/reserve-block', methods=['POST'])
def block_reservation():
    data = request.json
    company_id = data['company_id']
    reservations = data['reservations']  # list of dicts

    conn = get_db()
    with conn.cursor() as cursor:
        for res in reservations:
            cursor.execute("""
                INSERT INTO reservation (room_id, room_type, num_guests, arrival_date, departure_date, status, credit_card_provided, payment_status)
                VALUES (%s, %s, %s, %s, %s, 'confirmed', 0, 'pending')
            """, (res['room_id'], res['room_type'], res['num_guests'], res['arrival_date'], res['departure_date']))
            reservation_id = cursor.lastrowid
            cursor.execute("""
                INSERT INTO travel_company_reservation (reservation_id, company_id)
                VALUES (%s, %s)
            """, (reservation_id, company_id))
        conn.commit()
    return jsonify({"message": "Rooms successfully blocked for the travel company."})
