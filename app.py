# ===============================
# IMPORTS
# ===============================
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# ===============================
# APP CONFIGURATION
# ===============================
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hrm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ===============================
# DATABASE MODELS
# ===============================

class Department(db.Model):
    dept_id = db.Column(db.Integer, primary_key=True)
    dept_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))
    status = db.Column(db.String(50), default='active')


class Employee(db.Model):
    emp_id = db.Column(db.Integer, primary_key=True)
    emp_name = db.Column(db.String(100), nullable=False)
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


# ===============================
# DEPARTMENT ROUTES
# ===============================

@app.route('/')
def index():

    search = request.args.get('search')

    if search:
        departments = Department.query.filter(
            Department.dept_name.like(f"%{search}%"),
            Department.status == "active"
        ).all()
    else:
        departments = Department.query.filter_by(status="active").all()

    return render_template("index.html", departments=departments, count=len(departments))


@app.route('/add')
def add_page():
    return render_template("add_department.html")


@app.route('/add_department', methods=['POST'])
def add_department():

    dept_name = request.form['dept_name']
    description = request.form['description']

    new_dept = Department(
        dept_name=dept_name,
        description=description
    )

    db.session.add(new_dept)
    db.session.commit()

    return redirect('/')


@app.route('/delete/<int:id>')
def delete_department(id):

    dept = Department.query.get(id)
    dept.status = "inactive"

    db.session.commit()

    return redirect('/')


@app.route('/edit/<int:id>')
def edit_department(id):

    dept = Department.query.get(id)

    return render_template("edit_department.html", dept=dept)


@app.route('/update/<int:id>', methods=['POST'])
def update_department(id):

    dept = Department.query.get(id)

    dept.dept_name = request.form['dept_name']
    dept.description = request.form['description']

    db.session.commit()

    return redirect('/')


# ===============================
# EMPLOYEE ROUTES
# ===============================

@app.route('/employees')
def employees():

    search = request.args.get('search')

    if search:
        employees = Employee.query.filter(
            Employee.emp_name.like(f"%{search}%"),
            Employee.status == "active"
        ).all()
    else:
        employees = Employee.query.filter_by(status="active").all()

    return render_template("employees.html", employees=employees)


@app.route('/add_employee')
def add_employee_page():

    departments = Department.query.filter_by(status='active').all()

    return render_template("add_employee.html", departments=departments)


@app.route('/save_employee', methods=['POST'])
def save_employee():

    emp = Employee(
        emp_name=request.form['emp_name'],
        email=request.form['email'],
        phone=request.form['phone'],
        department_id=request.form['department_id']
    )

    db.session.add(emp)
    db.session.commit()

    return redirect('/employees')


@app.route('/employee/<int:id>')
def employee_profile(id):

    emp = Employee.query.get(id)

    return render_template("employee_profile.html", emp=emp)


@app.route('/delete_employee/<int:id>')
def delete_employee(id):

    emp = Employee.query.get(id)
    emp.status = "inactive"

    db.session.commit()

    return redirect('/employees')


@app.route('/edit_employee/<int:id>')
def edit_employee(id):

    emp = Employee.query.get(id)
    departments = Department.query.filter_by(status='active').all()

    return render_template("edit_employee.html", emp=emp, departments=departments)


@app.route('/update_employee/<int:id>', methods=['POST'])
def update_employee(id):

    emp = Employee.query.get(id)

    emp.emp_name = request.form['emp_name']
    emp.email = request.form['email']
    emp.phone = request.form['phone']
    emp.department_id = request.form['department_id']

    db.session.commit()

    return redirect('/employees')


# ===============================
# ATTENDANCE ROUTES
# ===============================

@app.route('/checkin/<int:id>')
def checkin(id):

    attendance = Attendance(emp_id=id)

    db.session.add(attendance)
    db.session.commit()

    return redirect('/employees')


@app.route('/checkout/<int:id>')
def checkout(id):

    attendance = Attendance.query.filter_by(
        emp_id=id,
        check_out=None
    ).first()

    if attendance:
        attendance.check_out = datetime.utcnow()
        db.session.commit()

    return redirect('/employees')


# ===============================
# DATABASE INITIALIZATION
# ===============================

with app.app_context():
    db.create_all()


# ===============================
# RUN APP
# ===============================

if __name__ == "__main__":
    app.run(debug=True)