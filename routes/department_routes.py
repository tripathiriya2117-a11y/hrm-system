from flask import Blueprint, render_template, request, redirect
from models import db, Department

department_bp = Blueprint('department', __name__)


# =========================
# Dashboard (MAIN PAGE)
# =========================
@department_bp.route('/dashboard')
def index():
    departments = Department.query.filter_by(status='active').all()
    return render_template("index.html", departments=departments)


# =========================
# Add Department Page
# =========================
@department_bp.route('/add')
def add_page():
    return render_template("add_department.html")


# =========================
# Save Department
# =========================
@department_bp.route('/add_department', methods=['POST'])
def add_department():

    dept = Department(
        dept_name=request.form['dept_name'],
        description=request.form['description']
    )

    db.session.add(dept)
    db.session.commit()

    return redirect('/dashboard')   


# =========================
# Delete Department (Soft)
# =========================
@department_bp.route('/delete/<int:id>')
def delete_department(id):

    dept = Department.query.get(id)
    dept.status = 'inactive'

    db.session.commit()

    return redirect('/dashboard')  


# =========================
# Edit Department Page
# =========================
@department_bp.route('/edit/<int:id>')
def edit_department(id):

    dept = Department.query.get(id)

    return render_template("edit_department.html", dept=dept)


# =========================
# Update Department
# =========================
@department_bp.route('/update/<int:id>', methods=['POST'])
def update_department(id):

    dept = Department.query.get(id)

    dept.dept_name = request.form['dept_name']
    dept.description = request.form['description']

    db.session.commit()

    return redirect('/dashboard')   