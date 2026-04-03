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
    emp_name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))

    department_id = db.Column(db.Integer, db.ForeignKey('department.dept_id'))
    department = db.relationship('Department')

    status = db.Column(db.String(50), default='active')

class Attendance(db.Model):
    att_id = db.Column(db.Integer, primary_key=True)

    emp_id = db.Column(db.Integer, db.ForeignKey('employee.emp_id'))
    employee = db.relationship('Employee')

    check_in = db.Column(db.DateTime, default=datetime.utcnow)
    check_out = db.Column(db.DateTime)

    date = db.Column(db.Date, default=datetime.utcnow)