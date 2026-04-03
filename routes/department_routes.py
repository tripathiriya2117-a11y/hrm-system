from flask import Blueprint, render_template, request, redirect
from models import db, Department

department_bp = Blueprint('department', __name__)


@department_bp.route('/')
def index():

    departments = Department.query.filter_by(status="active").all()

    return render_template("index.html", departments=departments)


@department_bp.route('/add')
def add_page():
    return render_template("add_department.html")


@department_bp.route('/add_department', methods=['POST'])
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


@department_bp.route('/delete/<int:id>')
def delete_department(id):

    dept = Department.query.get(id)
    dept.status = "inactive"

    db.session.commit()

    return redirect('/')


@department_bp.route('/edit/<int:id>')
def edit_department(id):

    dept = Department.query.get(id)

    return render_template("edit_department.html", dept=dept)


@department_bp.route('/update/<int:id>', methods=['POST'])
def update_department(id):

    dept = Department.query.get(id)

    dept.dept_name = request.form['dept_name']
    dept.description = request.form['description']

    db.session.commit()

    return redirect('/')