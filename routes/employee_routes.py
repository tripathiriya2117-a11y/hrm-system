from flask import Blueprint, render_template, request, redirect, session
from models import db, Employee, Department, Role
from datetime import datetime


# ✅ MUST COME FIRST
employee_bp = Blueprint('employee', __name__)


# =========================
# EMPLOYEE LIST
# =========================
@employee_bp.route('/employees')
def employees():
    employees = Employee.query.all()
    return render_template("employees.html", employees=employees)
# =========================
# Add Employee Page
# =========================
@employee_bp.route('/add_employee')
def add_employee_page():

    departments = Department.query.all()
    roles = Role.query.all()
    managers = Employee.query.filter_by(status='active').all()

    return render_template(
        "add_employee.html",
        departments=departments,
        roles=roles,
        managers=managers
    )


# =========================
# Save Employee
# =========================
@employee_bp.route('/save_employee', methods=['POST'])
def save_employee():

    reporting_manager_id = request.form.get('reporting_manager_id')
    reporting_manager_id = int(reporting_manager_id) if reporting_manager_id else None

    emp = Employee(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        username=request.form['username'],
        password=request.form['password'],
        email=request.form['email'],
        mobile=request.form['mobile'],
        dept_id=int(request.form['dept_id']),
        role_id=int(request.form['role_id']),
        reporting_manager_id=reporting_manager_id,
        date_of_joining=datetime.strptime(
            request.form['date_of_joining'],
            "%Y-%m-%d"
        ).date(),
        created_at=datetime.utcnow()
    )

    db.session.add(emp)
    db.session.commit()

    return redirect('/employees')


# =========================
# Delete Employee (soft delete)
# =========================
@employee_bp.route('/delete_employee/<int:id>')
def delete_employee(id):

    emp = Employee.query.get(id)
    emp.status = 'inactive'

    db.session.commit()

    return redirect('/employees')


# =========================
# Edit Employee Page
# =========================
@employee_bp.route('/edit_employee/<int:id>')
def edit_employee(id):

    emp = Employee.query.get(id)
    departments = Department.query.all()
    roles = Role.query.all()

    return render_template(
        "edit_employee.html",
        emp=emp,
        departments=departments,
        roles=roles
    )


# =========================
# Update Employee
# =========================
@employee_bp.route('/update_employee/<int:id>', methods=['POST'])
def update_employee(id):

    emp = Employee.query.get(id)

    emp.first_name = request.form['first_name']
    emp.last_name = request.form['last_name']
    emp.email = request.form['email']
    emp.mobile = request.form['mobile']
    emp.dept_id = request.form['dept_id']
    emp.role_id = request.form['role_id']

    emp.updated_at = datetime.utcnow()

    db.session.commit()

    return redirect('/employees')

@employee_bp.route('/employee/<int:id>')
def employee_profile(id):

    if 'user_id' not in session:
        return redirect('/login')

    emp = Employee.query.get(id)

    return render_template('employee_profile.html', emp=emp)
# ✅ MUST COME FIRST
employee_bp = Blueprint('employee', __name__)


# =========================
# EMPLOYEE LIST
# =========================
@employee_bp.route('/employees')
def employees():
    employees = Employee.query.all()
    return render_template("employees.html", employees=employees)
# =========================
# Add Employee Page
# =========================
@employee_bp.route('/add_employee')
def add_employee_page():

    departments = Department.query.all()
    roles = Role.query.all()
    managers = Employee.query.filter_by(status='active').all()

    return render_template(
        "add_employee.html",
        departments=departments,
        roles=roles,
        managers=managers
    )


# =========================
# Save Employee
# =========================
@employee_bp.route('/save_employee', methods=['POST'])
def save_employee():

    emp = Employee(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        username=request.form['username'],
        password=request.form['password'],
        email=request.form['email'],
        mobile=request.form['mobile'],
        dept_id=request.form['dept_id'],
        role_id=request.form['role_id'],
        reporting_manager_id=request.form.get('reporting_manager_id') or None,
        date_of_joining=datetime.strptime(
            request.form['date_of_joining'],
            "%Y-%m-%d"
        ).date(),
        created_at=datetime.utcnow()
    )

    db.session.add(emp)
    db.session.commit()

    return redirect('/employees')


# =========================
# Delete Employee (soft delete)
# =========================
@employee_bp.route('/delete_employee/<int:id>')
def delete_employee(id):

    emp = Employee.query.get(id)
    emp.status = 'inactive'

    db.session.commit()

    return redirect('/employees')


# =========================
# Edit Employee Page
# =========================
@employee_bp.route('/edit_employee/<int:id>')
def edit_employee(id):

    emp = Employee.query.get(id)
    departments = Department.query.all()
    roles = Role.query.all()

    return render_template(
        "edit_employee.html",
        emp=emp,
        departments=departments,
        roles=roles
    )


# =========================
# Update Employee
# =========================
@employee_bp.route('/update_employee/<int:id>', methods=['POST'])
def update_employee(id):

    emp = Employee.query.get(id)

    emp.first_name = request.form['first_name']
    emp.last_name = request.form['last_name']
    emp.email = request.form['email']
    emp.mobile = request.form['mobile']
    emp.dept_id = request.form['dept_id']
    emp.role_id = request.form['role_id']

    emp.updated_at = datetime.utcnow()

    db.session.commit()

    return redirect('/employees')

@employee_bp.route('/employee/<int:id>')
def employee_profile(id):

    if 'user_id' not in session:
        return redirect('/login')

    emp = Employee.query.get(id)

    return render_template('employee_profile.html', emp=emp)