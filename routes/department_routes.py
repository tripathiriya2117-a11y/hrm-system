from flask import Blueprint, render_template, request, redirect, session
from models import db, Department

department_bp = Blueprint('department', __name__)


# =========================
# Dashboard (MAIN PAGE)
# =========================
@department_bp.route('/dashboard')
def index():
     if 'user_id' not in session:
         return redirect('/login')

     departments = Department.query.filter_by(status='active').all()
     return render_template("index.html", departments=departments)

# =========================
# Add Department Page
# =========================
@department_bp.route('/add')
def add_page():

    if 'user_id' not in session:
        return redirect('/login')

    return render_template("add_department.html")


# =========================
# Save Department
# =========================
@department_bp.route('/add_department', methods=['POST'])
def add_department():

    if 'user_id' not in session:
       return redirect('/login')

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

    if 'user_id' not in session:
        return redirect('/login')

    dept = Department.query.get(id)

    if dept:
        dept.status = 'inactive'
        db.session.commit()

    return redirect('/dashboard')


# =========================
# Edit Department Page
# =========================
@department_bp.route('/edit/<int:id>')
def edit_department(id):

    if 'user_id' not in session:
        return redirect('/login')

    dept = Department.query.get(id)

    return render_template("edit_department.html", dept=dept)


# =========================
# Update Department
# =========================
@department_bp.route('/update/<int:id>', methods=['POST'])
def update_department(id):

    if 'user_id' not in session:
        return redirect('/login')

    dept = Department.query.get(id)

    if dept:
        dept.dept_name = request.form['dept_name']
        dept.description = request.form['description']
        db.session.commit()

    return redirect('/dashboard')