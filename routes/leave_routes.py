from flask import Blueprint, render_template, redirect, session, request
from models import db, Leave, Employee
from datetime import datetime

leave_bp = Blueprint('leave', __name__)


@leave_bp.route('/leave/apply')
def apply_leave_page():
    if 'user_id' not in session:
        return redirect('/login')

    return render_template('apply_leave.html')


@leave_bp.route('/leave/save', methods=['POST'])
def save_leave():

    leave = Leave(
        employee_id=session['user_id'],
        leave_type=request.form['leave_type'],
        reason=request.form['reason'],
        from_date=datetime.strptime(request.form['from_date'], '%Y-%m-%d'),
        to_date=datetime.strptime(request.form['to_date'], '%Y-%m-%d'),
        created_at=datetime.utcnow()
    )

    db.session.add(leave)
    db.session.commit()

    return redirect('/leave/dashboard')


@leave_bp.route('/leave/dashboard')
def leave_dashboard():

    if 'user_id' not in session:
        return redirect('/login')

    leaves = Leave.query.all()

    return render_template('leave_dashboard.html', leaves=leaves)


@leave_bp.route('/leave/update/<int:id>/<status>')
def update_leave(id, status):

    leave = Leave.query.get(id)
    leave.status = status

    db.session.commit()

    return redirect('/leave/dashboard')

