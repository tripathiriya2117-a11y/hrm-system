from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Department(db.Model):
    dept_id = db.Column(db.Integer, primary_key=True)
    dept_name = db.Column(db.String(100))
    description = db.Column(db.String(300))
    status = db.Column(db.String(50), default='active')

class Employee(db.Model):

    emp_id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

    email = db.Column(db.String(120))
    mobile = db.Column(db.String(20))

    dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'))

    reporting_manager_id = db.Column(db.Integer, db.ForeignKey('employee.emp_id'))

    date_of_joining = db.Column(db.Date)

    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    status = db.Column(db.String(50), default='active')
    
class Attendance(db.Model):
    att_id = db.Column(db.Integer, primary_key=True)

    emp_id = db.Column(db.Integer, db.ForeignKey('employee.emp_id'))
    employee = db.relationship('Employee')

    check_in = db.Column(db.DateTime, default=datetime.utcnow)
    check_out = db.Column(db.DateTime)

    date = db.Column(db.Date, default=datetime.utcnow)

class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    status = db.Column(db.String(50), default='active')
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)    