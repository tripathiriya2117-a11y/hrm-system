from flask import Blueprint, render_template, redirect
from models import db, Attendance
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__)


@attendance_bp.route('/checkin/<int:id>')
def checkin(id):

    attendance = Attendance(
        emp_id=id
    )

    db.session.add(attendance)
    db.session.commit()

    return redirect('/employees')


@attendance_bp.route('/checkout/<int:id>')
def checkout(id):

    attendance = Attendance.query.filter_by(
        emp_id=id,
        check_out=None
    ).first()

    if attendance:
        attendance.check_out = datetime.utcnow()
        db.session.commit()

    return redirect('/employees')


@attendance_bp.route('/attendance')
def attendance():

    attendance = Attendance.query.all()

    return render_template("attendance.html", attendance=attendance)