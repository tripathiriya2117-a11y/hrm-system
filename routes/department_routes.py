from flask import Blueprint, render_template, request, redirect
from models import db, Department

department_bp = Blueprint('department', __name__)


@department_bp.route('/')
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