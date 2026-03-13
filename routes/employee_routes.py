from flask import Blueprint, render_template, request, redirect
from models import db, Employee, Department

# Blueprint for employee module
employee_bp = Blueprint('employee', __name__)


@employee_bp.route('/employees')
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


@employee_bp.route('/add_employee')
def add_employee_page():

    departments = Department.query.filter_by(status='active').all()

    return render_template("add_employee.html", departments=departments)


@employee_bp.route('/save_employee', methods=['POST'])
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


@employee_bp.route('/employee/<int:id>')
def employee_profile(id):

    emp = Employee.query.get(id)

    return render_template("employee_profile.html", emp=emp)


@employee_bp.route('/delete_employee/<int:id>')
def delete_employee(id):

    emp = Employee.query.get(id)
    emp.status = "inactive"

    db.session.commit()

    return redirect('/employees')


@employee_bp.route('/edit_employee/<int:id>')
def edit_employee(id):

    emp = Employee.query.get(id)
    departments = Department.query.filter_by(status='active').all()

    return render_template("edit_employee.html", emp=emp, departments=departments)


@employee_bp.route('/update_employee/<int:id>', methods=['POST'])
def update_employee(id):

    emp = Employee.query.get(id)

    emp.emp_name = request.form['emp_name']
    emp.email = request.form['email']
    emp.phone = request.form['phone']
    emp.department_id = request.form['department_id']

    db.session.commit()

    return redirect('/employees')