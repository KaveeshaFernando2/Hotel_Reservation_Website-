from flask import Blueprint, render_template, request, jsonify, current_app
import pymysql

manager_bp = Blueprint('manager', __name__)

def get_db_connection():
    db_config = current_app.config['DB_CONFIG']
    connection = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

@manager_bp.route('/manager/reports')
def manager_reports():
    return render_template('manager_reports.html')

@manager_bp.route('/api/reports/occupancy')
def occupancy_report():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) AS total_rooms,
                       SUM(CASE WHEN status = 'confirmed' THEN 1 ELSE 0 END) AS occupied_rooms
                FROM reservation
                WHERE arrival_date <= CURDATE() AND departure_date >= CURDATE();
            """)
            result = cursor.fetchone()
            return jsonify(result)
    finally:
        conn.close()

@manager_bp.route('/api/reports/projected')
def projected_occupancy():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT DATE(arrival_date) AS date, COUNT(*) AS bookings
                FROM reservation
                WHERE arrival_date > CURDATE() AND status = 'paid'
                GROUP BY DATE(arrival_date)
                ORDER BY DATE(arrival_date);
            """)
            result = cursor.fetchall()
            return jsonify(result)
    finally:
        conn.close()

@manager_bp.route('/api/reports/financial')
def financial_report():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if start_date and end_date:
                cursor.execute("""
                    SELECT IFNULL(SUM(rm.price_per_night), 0) AS total_revenue
                    FROM reservation r
                    JOIN room rm ON r.room_id = rm.id
                    WHERE r.status = 'paid' AND r.arrival_date BETWEEN %s AND %s;
                """, (start_date, end_date))
            else:
                cursor.execute("""
                    SELECT IFNULL(SUM(rm.price_per_night), 0) AS total_revenue
                    FROM reservation r
                    JOIN room rm ON r.room_id = rm.id
                    WHERE r.status = 'paid';
                """)
            result = cursor.fetchone()
            return jsonify(result)
    finally:
        conn.close()



