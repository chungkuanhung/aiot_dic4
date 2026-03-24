import sqlite3
import time
import random
import datetime
import os

DB_NAME = "aiotdb.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # 1. 建立 sensors 資料表 (如果不存在的話)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            temperature REAL,
            humidity REAL
        )
    ''')
    conn.commit()
    conn.close()
    print("已經確認 SQLite 資料庫 `sensors` 表格建立完成。")

def generate_and_insert():
    # 開啟連線
    conn = sqlite3.connect(DB_NAME, timeout=10)
    cursor = conn.cursor()
    
    print("啟動虛擬感測器資料產生器... 每 2 秒寫入一次資料 (按 Ctrl+C 停止)")
    try:
        while True:
            # 2. 隨機產生溫濕度
            temperature = round(random.uniform(20.0, 35.0), 2)
            humidity = round(random.uniform(40.0, 70.0), 2)
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 1. 將資料 insert 到 SQLite3 aiotdb.db 的 sensors 表格中
            cursor.execute('''
                INSERT INTO sensors (timestamp, temperature, humidity) 
                VALUES (?, ?, ?)
            ''', (current_time, temperature, humidity))
            
            conn.commit()
            print(f"[{current_time}] 新增資料: 溫度={temperature}°C, 濕度={humidity}%")
            
            # 2. 每 2 秒產生一次資料
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n收到中斷訊號，停止寫入資料。")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
    generate_and_insert()
