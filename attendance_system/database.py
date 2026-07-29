import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'attendance.db')


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_number TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            class_name TEXT NOT NULL,
            section TEXT,
            email TEXT,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Attendance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            date DATE NOT NULL,
            status TEXT CHECK(status IN ('Present', 'Absent', 'Late')),
            subject TEXT,
            marked_by TEXT,
            marked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id),
            UNIQUE(student_id, date, subject)
        )
    ''')
    
    # Subjects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            code TEXT UNIQUE
        )
    ''')
    
    # Insert sample subjects
    subjects = [('Mathematics', 'MATH101'), ('Physics', 'PHY101'), 
                ('Chemistry', 'CHEM101'), ('Computer Science', 'CS101')]
    cursor.executemany('INSERT OR IGNORE INTO subjects (name, code) VALUES (?, ?)', subjects)
    
    conn.commit()
    conn.close()

# Student CRUD operations
def add_student(roll_number, name, class_name, section, email, phone):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO students (roll_number, name, class_name, section, email, phone)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (roll_number, name, class_name, section, email, phone))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students ORDER BY roll_number')
    students = cursor.fetchall()
    conn.close()
    return students

def get_student_by_id(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
    student = cursor.fetchone()
    conn.close()
    return student

def update_student(student_id, roll_number, name, class_name, section, email, phone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE students 
        SET roll_number=?, name=?, class_name=?, section=?, email=?, phone=?
        WHERE id=?
    ''', (roll_number, name, class_name, section, email, phone, student_id))
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
    cursor.execute('DELETE FROM attendance WHERE student_id = ?', (student_id,))
    conn.commit()
    conn.close()

# Attendance operations
def mark_attendance(student_id, date, status, subject, marked_by):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO attendance (student_id, date, status, subject, marked_by)
            VALUES (?, ?, ?, ?, ?)
        ''', (student_id, date, status, subject, marked_by))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        cursor.execute('''
            UPDATE attendance 
            SET status=?, marked_by=?, marked_at=CURRENT_TIMESTAMP
            WHERE student_id=? AND date=? AND subject=?
        ''', (status, marked_by, student_id, date, subject))
        conn.commit()
        return True
    finally:
        conn.close()

def get_attendance_by_date(date, subject=None):
    conn = get_connection()
    cursor = conn.cursor()
    if subject:
        cursor.execute('''
            SELECT s.id, s.roll_number, s.name, a.status, a.marked_at
            FROM students s
            LEFT JOIN attendance a ON s.id = a.student_id AND a.date = ? AND a.subject = ?
            ORDER BY s.roll_number
        ''', (date, subject))
    else:
        cursor.execute('''
            SELECT s.id, s.roll_number, s.name, a.status, a.marked_at
            FROM students s
            LEFT JOIN attendance a ON s.id = a.student_id AND a.date = ?
            ORDER BY s.roll_number
        ''', (date,))
    attendance = cursor.fetchall()
    conn.close()
    return attendance

def get_student_attendance_summary(student_id, start_date=None, end_date=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT 
            COUNT(*) as total_days,
            SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) as present_count,
            SUM(CASE WHEN status = 'Absent' THEN 1 ELSE 0 END) as absent_count,
            SUM(CASE WHEN status = 'Late' THEN 1 ELSE 0 END) as late_count,
            ROUND(CAST(SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) as percentage
        FROM attendance
        WHERE student_id = ?
    '''
    params = [student_id]
    
    if start_date and end_date:
        query += ' AND date BETWEEN ? AND ?'
        params.extend([start_date, end_date])
    
    cursor.execute(query, params)
    summary = cursor.fetchone()
    conn.close()
    return summary

def get_subjects():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM subjects ORDER BY name')
    subjects = [row[0] for row in cursor.fetchall()]
    conn.close()
    return subjects

def get_class_attendance_report(class_name, start_date=None, end_date=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT 
            s.roll_number,
            s.name,
            COUNT(*) as total_days,
            SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) as present_count,
            SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END) as absent_count,
            SUM(CASE WHEN a.status = 'Late' THEN 1 ELSE 0 END) as late_count,
            ROUND(CAST(SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) as percentage
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id
        WHERE s.class_name = ?
    '''
    params = [class_name]
    
    if start_date and end_date:
        query += ' AND a.date BETWEEN ? AND ?'
        params.extend([start_date, end_date])
    
    query += ' GROUP BY s.id ORDER BY s.roll_number'
    
    cursor.execute(query, params)
    report = cursor.fetchall()
    conn.close()
    return report

def search_students(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM students 
        WHERE roll_number LIKE ? OR name LIKE ? OR email LIKE ?
        ORDER BY roll_number
    ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
    students = cursor.fetchall()
    conn.close()
    return students

def get_date_range_attendance(start_date, end_date, student_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    if student_id:
        cursor.execute('''
            SELECT date, status, subject, marked_by
            FROM attendance
            WHERE student_id = ? AND date BETWEEN ? AND ?
            ORDER BY date DESC
        ''', (student_id, start_date, end_date))
    else:
        cursor.execute('''
            SELECT s.id, s.roll_number, s.name, a.date, a.status, a.subject
            FROM students s
            LEFT JOIN attendance a ON s.id = a.student_id
            WHERE a.date BETWEEN ? AND ?
            ORDER BY s.roll_number, a.date DESC
        ''', (start_date, end_date))
    
    results = cursor.fetchall()
    conn.close()
    return results

def get_today_attendance_status():
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().date().isoformat()
    cursor.execute('''
        SELECT s.id, s.roll_number, s.name, a.status
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id AND a.date = ?
        ORDER BY s.roll_number
    ''', (today,))
    results = cursor.fetchall()
    conn.close()
    return results