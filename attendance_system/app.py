from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, date
import database

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Initialize database
database.init_database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    students = database.get_all_students()
    total_students = len(students)
    
    # Today's attendance summary
    today = date.today().isoformat()
    today_attendance = database.get_attendance_by_date(today)
    present_today = sum(1 for record in today_attendance if record[3] == 'Present')
    absent_today = sum(1 for record in today_attendance if record[3] == 'Absent')
    
    # Overall attendance percentage (first student as sample)
    if total_students > 0:
        summary = database.get_student_attendance_summary(students[0][0])
        overall_percentage = summary[4] if summary and summary[4] else 0
    else:
        overall_percentage = 0
    
    return render_template('dashboard.html', 
                         total_students=total_students,
                         present_today=present_today,
                         absent_today=absent_today,
                         overall_percentage=overall_percentage)

@app.route('/students')
def students():
    students_list = database.get_all_students()
    return render_template('students.html', students=students_list)

@app.route('/add_student', methods=['POST'])
def add_student():
    roll_number = request.form['roll_number']
    name = request.form['name']
    class_name = request.form['class_name']
    section = request.form['section']
    email = request.form['email']
    phone = request.form['phone']
    
    if database.add_student(roll_number, name, class_name, section, email, phone):
        flash('Student added successfully!', 'success')
    else:
        flash('Student with this roll number already exists!', 'danger')
    
    return redirect(url_for('students'))

@app.route('/edit_student/<int:student_id>', methods=['POST'])
def edit_student(student_id):
    roll_number = request.form['roll_number']
    name = request.form['name']
    class_name = request.form['class_name']
    section = request.form['section']
    email = request.form['email']
    phone = request.form['phone']
    
    database.update_student(student_id, roll_number, name, class_name, section, email, phone)
    flash('Student updated successfully!', 'success')
    return redirect(url_for('students'))

@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):
    database.delete_student(student_id)
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('students'))

@app.route('/take_attendance', methods=['GET', 'POST'])
def take_attendance():
    subjects = database.get_subjects()
    
    if request.method == 'POST':
        attendance_date = request.form['date']
        subject = request.form['subject']
        marked_by = request.form['marked_by']
        
        for key, value in request.form.items():
            if key.startswith('status_'):
                student_id = key.split('_')[1]
                if value:
                    database.mark_attendance(student_id, attendance_date, value, subject, marked_by)
        
        flash('Attendance marked successfully!', 'success')
        return redirect(url_for('view_attendance', date=attendance_date, subject=subject))
    
    today = date.today().isoformat()
    students_list = database.get_all_students()
    return render_template('take_attendance.html', 
                         students=students_list, 
                         subjects=subjects,
                         today=today)

@app.route('/view_attendance')
def view_attendance():
    date_param = request.args.get('date', date.today().isoformat())
    subject_param = request.args.get('subject', '')
    
    subjects = database.get_subjects()
    attendance_records = database.get_attendance_by_date(date_param, subject_param if subject_param else None)
    
    return render_template('view_attendance.html', 
                         attendance=attendance_records,
                         date=date_param,
                         subjects=subjects,
                         selected_subject=subject_param)

@app.route('/reports')
def reports():
    students_list = database.get_all_students()
    reports_data = []
    
    for student in students_list:
        summary = database.get_student_attendance_summary(student[0])
        if summary and summary[0] > 0:
            reports_data.append({
                'roll_number': student[1],
                'name': student[2],
                'class': student[3],
                'section': student[4],
                'total_days': summary[0],
                'present': summary[1],
                'absent': summary[2],
                'late': summary[3],
                'percentage': summary[4]
            })
    
    return render_template('reports.html', reports=reports_data)

@app.route('/api/attendance_summary/<int:student_id>')
def api_attendance_summary(student_id):
    summary = database.get_student_attendance_summary(student_id)
    return jsonify({
        'total_days': summary[0],
        'present': summary[1],
        'absent': summary[2],
        'late': summary[3],
        'percentage': summary[4]
    })

if __name__ == '__main__':
    app.run(debug=True)