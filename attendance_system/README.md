# Student Attendance System

A modern, feature-rich web application for tracking and managing student attendance with comprehensive reporting capabilities.

## Features

### 📊 Dashboard
- Real-time attendance statistics
- Today's attendance summary (Present, Absent, Not Marked)
- Overall attendance percentage
- Interactive charts and visualizations
- Quick action buttons for common tasks

### 👥 Student Management
- Add new students with complete details
- Edit student information
- Delete student records
- View all enrolled students
- Store student details (name, roll number, class, section, email, phone)

### 📋 Attendance Marking
- Mark attendance by date and subject
- Quick status selection (Present, Absent, Late)
- Bulk operations (Mark All Present/Absent)
- Multiple subject support
- Track attendance by teacher/staff member

### 📰 Attendance Viewing
- Filter attendance by date and subject
- View detailed attendance records
- Display attendance status with color-coded badges
- Summary statistics for each date

### 📈 Reports & Analytics
- Comprehensive student attendance reports
- Attendance percentage calculations
- Status indicators (Good, Average, Poor)
- Visual progress bars
- Export to CSV functionality
- Print-friendly reports

## Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite3 (lightweight, file-based)
- **Python Version**: 3.x

### Frontend
- **UI Framework**: Bootstrap 5
- **Icons**: Bootstrap Icons
- **Charts**: Chart.js
- **Styling**: Custom CSS with gradients and animations

## Installation

### Prerequisites
- Python 3.x
- pip (Python package manager)

### Setup Steps

1. **Clone or download the repository**
   ```bash
   cd attendance_system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000`
   - The application will automatically initialize the database

## Project Structure

```
attendance_system/
├── app.py                  # Main Flask application
├── database.py             # Database operations and queries
├── requirements.txt        # Python dependencies
├── static/
│   └── style.css          # Custom styling
└── templates/
    ├── base.html          # Base template with navigation
    ├── index.html         # Home/landing page
    ├── dashboard.html     # Dashboard with statistics
    ├── students.html      # Student management
    ├── take_attendance.html # Mark attendance
    ├── view_attendance.html # View attendance records
    └── reports.html       # Attendance reports
```

## Database Schema

### Students Table
- `id`: Unique identifier (Primary Key)
- `roll_number`: Student roll number (Unique)
- `name`: Full name
- `class_name`: Class/Grade
- `section`: Section/Division
- `email`: Email address
- `phone`: Phone number
- `created_at`: Timestamp of record creation

### Attendance Table
- `id`: Unique identifier (Primary Key)
- `student_id`: Foreign key to Students
- `date`: Attendance date
- `status`: Present/Absent/Late
- `subject`: Subject name
- `marked_by`: Name of teacher/staff
- `marked_at`: Timestamp of marking

### Subjects Table
- `id`: Unique identifier (Primary Key)
- `name`: Subject name
- `code`: Subject code

## Usage Guide

### Adding Students
1. Navigate to the **Students** page
2. Fill in the student details in the "Add New Student" form
3. Click the **Add Student** button
4. Student will appear in the student records table

### Taking Attendance
1. Go to the **Take Attendance** page
2. Select the date, subject, and mark who's taking the attendance
3. For each student, select their status (Present/Absent/Late)
4. Use quick buttons to mark all as present or absent
5. Click **Save Attendance** to record the data

### Viewing Attendance
1. Visit the **View Attendance** page
2. Filter by date and subject (optional)
3. Click **Filter** to see attendance records
4. Records are displayed with color-coded status badges

### Generating Reports
1. Navigate to the **Reports** page
2. View comprehensive attendance summary for all students
3. Attendance percentage is color-coded:
   - **Green**: ≥75% (Good)
   - **Yellow**: 60-74% (Average)
   - **Red**: <60% (Poor)
4. Export data to CSV or print the report

## Features Highlight

### User Interface
- ✨ Modern, responsive design
- 🎨 Beautiful gradients and smooth animations
- 📱 Mobile-friendly layout
- ⚡ Fast and interactive

### Database Features
- 🔒 Data integrity with foreign keys
- 🔄 Atomic transactions
- 📊 Efficient queries
- 🗂️ Organized schema

### Functionality
- ✅ Complete CRUD operations
- 📈 Real-time statistics
- 🎯 Bulk operations support
- 📥 Data export capability
- 🔍 Search and filter options

## Configuration

### Changing the Port
Open `app.py` and modify the last line:
```python
if __name__ == '__main__':
    app.run(debug=True, port=8000)  # Change 5000 to your desired port
```

### Changing the Secret Key
In `app.py`, update:
```python
app.secret_key = 'your_secret_key_here'  # Change to a secure random string
```

### Database Location
The SQLite database (`attendance.db`) is created in the application directory by default.

## Security Notes

- 🔐 Use a strong secret key in production
- 🛡️ Implement authentication for real-world deployment
- 🔒 Use HTTPS in production
- 📝 Regular database backups recommended
- ⚠️ Validate and sanitize all user inputs in production

## Troubleshooting

### Port Already in Use
```bash
# Use a different port
python app.py  # Edit app.py to change the port
```

### Database Locked Error
- Close other instances of the application
- Delete `attendance.db` and restart (loses all data)

### Missing Dependencies
```bash
pip install -r requirements.txt
```

### Flask Not Found
```bash
pip install Flask
```

## Future Enhancements

- 🔐 User authentication and authorization
- 🎓 Multi-class/multi-school support
- 📧 Email notifications for low attendance
- 📱 Mobile app integration
- 🗺️ Geolocation-based attendance
- 📊 Advanced analytics and predictions
- 🔗 API endpoints for third-party integration
- 📂 Backup and restore functionality

## License

This project is free to use for educational purposes.

## Support

For issues, suggestions, or improvements, please contact the development team.

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: Production Ready
