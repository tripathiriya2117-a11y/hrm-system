from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hrm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Department Table
class Department(db.Model):

    dept_id = db.Column(db.Integer, primary_key=True)
    dept_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))
    status = db.Column(db.String(50), default='active')


# Dashboard
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

# Add Department Page
@app.route('/add')
def add_page():
    return render_template("add_department.html")


# Insert Department
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


# Delete Department (soft delete)
@app.route('/delete/<int:id>')
def delete_department(id):

    dept = Department.query.get(id)
    dept.status = "inactive"

    db.session.commit()

    return redirect('/')


# Edit Department
@app.route('/edit/<int:id>')
def edit_department(id):

    dept = Department.query.get(id)

    return render_template("edit_department.html", dept=dept)


# Update Department
@app.route('/update/<int:id>', methods=['POST'])
def update_department(id):

    dept = Department.query.get(id)

    dept.dept_name = request.form['dept_name']
    dept.description = request.form['description']

    db.session.commit()

    return redirect('/')


# Create database automatically
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)