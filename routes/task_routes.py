from flask import Blueprint, render_template, request, redirect, session
from models import db, Task, TaskAssignment, Employee
from datetime import datetime

task_bp = Blueprint('task', __name__)

# =========================
# ADD TASK PAGE
# =========================
@task_bp.route('/task/add')
def add_task_page():

    if 'user_id' not in session:
        return redirect('/login')

    employees = Employee.query.all()
    return render_template('add_task.html', employees=employees)


# =========================
# SAVE TASK
# =========================
@task_bp.route('/task/save', methods=['POST'])
def save_task():

    if 'user_id' not in session:
        return redirect('/login')

    task = Task(
        title=request.form['title'],
        description=request.form['description'],
        priority=request.form['priority'],
        start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d'),
        end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d'),
        task_type=request.form['task_type']
    )

    db.session.add(task)
    db.session.commit()

    assignment = TaskAssignment(
        task_id=task.task_id,
        employee_id=int(request.form['employee_id']),
        assigned_by=session['user_id'],
        status='Pending'
    )

    db.session.add(assignment)
    db.session.commit()

    return redirect('/task/dashboard')   # ✅ FIXED


# =========================
# TASK DASHBOARD
# =========================
@task_bp.route('/task/dashboard')
def task_dashboard():

    if 'user_id' not in session:
        return redirect('/login')

    # Get filter values
    employee_id = request.args.get('employee_id')
    status = request.args.get('status')

    query = db.session.query(
        TaskAssignment, Task, Employee
    ).join(Task, Task.task_id == TaskAssignment.task_id)\
     .join(Employee, Employee.emp_id == TaskAssignment.employee_id)

    # Apply filters
    if employee_id:
        query = query.filter(TaskAssignment.employee_id == int(employee_id))

    if status:
        query = query.filter(TaskAssignment.status == status)

    data = query.all()

    employees = Employee.query.all()

    return render_template(
        'task_dashboard.html',
        data=data,
        employees=employees
    )
@task_bp.route('/task/complete/<int:id>')
def complete_task(id):

    if 'user_id' not in session:
        return redirect('/login')

    assignment = TaskAssignment.query.get(id)

    if assignment:
        assignment.status = "Completed"
        assignment.completed_at = datetime.now()
        db.session.commit()

    return redirect('/task/dashboard')