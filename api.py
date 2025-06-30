from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Cho phép truy cập từ trình duyệt khác port

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'summer_schema',
    'charset': 'utf8mb4'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/vote', methods=['POST'])
def vote():
    data = request.get_json()
    name = data.get('name', '').strip()
    choice = data.get('choice', '').strip()
    if not name or not choice:
        return jsonify({'success': False, 'message': 'Thiếu tên hoặc lựa chọn'}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Kiểm tra đã vote chưa
    cursor.execute("SELECT * FROM data WHERE Tên = %s", (name,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'message': 'Bạn đã bình chọn rồi!'})

    # Lưu bình chọn mới
    cursor.execute("INSERT INTO data (Tên, `Lựa chọn`) VALUES (%s, %s)", (name, choice))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Bình chọn thành công!'})

@app.route('/votes', methods=['GET'])
def get_votes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT `Lựa chọn`, COUNT(*) as count FROM data GROUP BY `Lựa chọn`")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)