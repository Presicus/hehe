from flask import Flask, jsonify, render_template
from flask_cors import CORS
import pyodbc
import pandas as pd
import threading
import time
import numpy as np  # Thêm thư viện numpy để xử lý NaT

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=172.30.59.57,1433;'
        'DATABASE=giuxe;'
        'UID=HUAN;'
        'PWD=HUAN;'
    )
    return conn

def update_db():
    while True:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Ví dụ cập nhật dữ liệu, chỉnh sửa theo nhu cầu của bạn
        cursor.execute("UPDATE baigiuxe SET column_name = column_name + 1 WHERE condition_column = 'condition_value'")
        conn.commit()
        conn.close()
        print("Database updated")
        time.sleep(10)  # Chờ 10 giây trước khi thực hiện cập nhật tiếp theo

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def get_data():
    conn = get_db_connection()
    query = "SELECT [Giờ ra bãi], [Giờ vào bãi], [Họ và tên], ID FROM baigiuxe"
    
    df = pd.read_sql(query, conn)
    
    # Xử lý NaT thành None (null) trong DataFrame
    df.replace({pd.NaT: None}, inplace=True)
    
    conn.close()
    
    # Chuyển đổi DataFrame thành dict và trả về dữ liệu dưới dạng JSON
    data = df.to_dict(orient='records')
    return jsonify(data)

if __name__ == '__main__':
    # Tạo và bắt đầu thread để cập nhật cơ sở dữ liệu liên tục
    db_thread = threading.Thread(target=update_db)
    db_thread.daemon = True
    db_thread.start()

    # Chạy Flask server
    app.run(debug=True)
