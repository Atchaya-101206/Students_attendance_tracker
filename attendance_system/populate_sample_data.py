#!/usr/bin/env python3
"""
Sample Data Generator for Student Attendance System
This script creates sample students and attendance records for testing purposes.
"""

import database
from datetime import datetime, timedelta
import random

def populate_sample_data():
    """Generate sample students and attendance records"""
    
    # Sample student data
    students_data = [
        ('STU001', 'Rajesh Kumar', '10A', 'A', 'rajesh@school.com', '9876543210'),
        ('STU002', 'Priya Singh', '10A', 'A', 'priya@school.com', '9876543211'),
        ('STU003', 'Amit Patel', '10A', 'A', 'amit@school.com', '9876543212'),
        ('STU004', 'Anjali Gupta', '10A', 'A', 'anjali@school.com', '9876543213'),
        ('STU005', 'Vikram Sharma', '10A', 'A', 'vikram@school.com', '9876543214'),
        ('STU006', 'Neha Desai', '10B', 'B', 'neha@school.com', '9876543215'),
        ('STU007', 'Arjun Verma', '10B', 'B', 'arjun@school.com', '9876543216'),
        ('STU008', 'Deepak Singh', '10B', 'B', 'deepak@school.com', '9876543217'),
        ('STU009', 'Rashi Malhotra', '10B', 'B', 'rashi@school.com', '9876543218'),
        ('STU010', 'Sanjay Roy', '10B', 'B', 'sanjay@school.com', '9876543219'),
    ]
    
    # Add students
    print("Adding students to the system...")
    added_count = 0
    for roll, name, class_name, section, email, phone in students_data:
        if database.add_student(roll, name, class_name, section, email, phone):
            print(f"✓ Added: {name} ({roll})")
            added_count += 1
        else:
            print(f"✗ Student {roll} already exists")
    
    print(f"\nTotal students added: {added_count}/{len(students_data)}")
    
    # Generate sample attendance records
    print("\nGenerating sample attendance records...")
    
    students = database.get_all_students()
    subjects = database.get_subjects()
    
    if not subjects:
        print("No subjects found. Please ensure database is initialized properly.")
        return
    
    # Generate attendance for last 30 days
    today = datetime.now().date()
    attendance_count = 0
    
    for days_back in range(30):
        current_date = (today - timedelta(days=days_back)).isoformat()
        
        # Skip weekends (Saturday=5, Sunday=6)
        day_of_week = (today - timedelta(days=days_back)).weekday()
        if day_of_week >= 5:  # Skip weekends
            continue
        
        for student in students:
            student_id = student[0]
            # Randomly select status with realistic distribution
            rand = random.random()
            if rand < 0.85:
                status = 'Present'
            elif rand < 0.95:
                status = 'Absent'
            else:
                status = 'Late'
            
            # Select a random subject
            subject = random.choice(subjects)
            
            # Mark attendance
            database.mark_attendance(student_id, current_date, status, subject, 'Staff')
            attendance_count += 1
    
    print(f"Total attendance records created: {attendance_count}")
    print("\n✓ Sample data populated successfully!")
    print("\nYou can now:")
    print("1. Visit http://localhost:5000/dashboard to see statistics")
    print("2. Go to http://localhost:5000/reports to view attendance reports")
    print("3. Check http://localhost:5000/students to see all students")

if __name__ == '__main__':
    print("=" * 60)
    print("Student Attendance System - Sample Data Generator")
    print("=" * 60)
    print("\nInitializing database...")
    database.init_database()
    print("Database initialized successfully!\n")
    
    populate_sample_data()
    
    print("\n" + "=" * 60)
    print("Setup complete! Visit http://localhost:5000 to start using the system.")
    print("=" * 60)
