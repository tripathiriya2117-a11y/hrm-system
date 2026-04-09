from flask import Blueprint, render_template, redirect
from models import db, Attendance
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/attendance/add')
def add_attendance():

    if 'user_id' not in session:
        return redirect('/login')

    employees = Employee.query.all()
    return render_template('add_attendance.html', employees=employees)

@attendance_bp.route('/checkin/<int:id>')
def checkin(id):
    db.session.add(Attendance(emp_id=id))
    db.session.commit()
    return redirect('/employees')

@attendance_bp.route('/checkout/<int:id>')
def checkout(id):
    att = Attendance.query.filter_by(emp_id=id, check_out=None).first()
    if att:
        att.check_out = datetime.utcnow()
        db.session.commit()
    return redirect('/employees')

@attendance_bp.route('/attendance')
def attendance():
    data = Attendance.query.all()
    return render_template("attendance.html", attendance=data)

from datetime import datetime

@attendance_bp.route('/attendance/save', methods=['POST'])
def save_attendance():

    if 'user_id' not in session:
        return redirect('/login')

    attendance = Attendance(
        employee_id=request.form['employee_id'],
        date=datetime.strptime(request.form['date'], '%Y-%m-%d'),
        status=request.form['status'],
        created_at=datetime.now()
    )

    db.session.add(attendance)
    db.session.commit()

    return redirect('/attendance')