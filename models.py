# models.py
import sqlite3
from config import Config
from datetime import datetime
import pytz

VN_TZ = pytz.timezone('Asia/Ho_Chi_Minh')

def get_db_connection():
    """Tạo kết nối database"""
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Khởi tạo database và bảng events"""
    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT ,
            start_time DATETIME ,
            end_time DATETIME ,
            location TEXT,
            reminder_minutes INTEGER DEFAULT 0,
            isComplete INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_all_events():
    """Lấy tất cả sự kiện, sắp xếp theo start_time"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events ORDER BY start_time ASC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_event_by_id(event_id):
    """Lấy một sự kiện theo ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events WHERE id = ?', (event_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def add_event(event_name, start_time_str, end_time_str, location, reminder_minutes):
    """Thêm sự kiện mới"""
    try:
        start_time = datetime.fromisoformat(start_time_str.replace('T', ' ')).replace(tzinfo=VN_TZ)
        if end_time_str :
            end_time = datetime.fromisoformat(end_time_str.replace('T', ' ')).replace(tzinfo=VN_TZ)
        else :
            end_time = None
    except ValueError:
        return None

    if end_time and end_time <= start_time:
        return None

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO events 
        (event, start_time, end_time, location, reminder_minutes, isComplete)
        VALUES (?, ?, ?, ?, ?, 0)
    ''', (event_name, start_time.isoformat(), end_time.isoformat() if end_time_str else None , location, reminder_minutes))
    conn.commit()

    new_id = cursor.lastrowid
    conn.close()
    return new_id

def toggle_complete(event_id):
    """Đổi trạng thái hoàn thành"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT isComplete FROM events WHERE id = ?', (event_id,))
    row = cursor.fetchone()
    if row:
        new_status = 0 if row['isComplete'] else 1
        cursor.execute('UPDATE events SET isComplete = ? WHERE id = ?', (new_status, event_id))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

# models.py
def update_event(event_id, event_name, start_time_str, end_time_str, location, reminder_minutes):
    """Cập nhật sự kiện"""
    try:
        start_time = datetime.fromisoformat(start_time_str.replace('T', ' ')).replace(tzinfo=VN_TZ)
        if end_time_str:
            end_time = datetime.fromisoformat(end_time_str.replace('T', ' ')).replace(tzinfo=VN_TZ)
        else:
            end_time = None
    except:
        return False

    if end_time and end_time <= start_time:
        return False

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE events 
        SET event = ?, start_time = ?, end_time = ?, location = ?, reminder_minutes = ?
        WHERE id = ?
    ''', (event_name, start_time.isoformat(), end_time.isoformat() if end_time_str else None, location or None, reminder_minutes, event_id))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


def delete_event(event_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM events WHERE id = ?', (event_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0