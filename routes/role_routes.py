from flask import Blueprint, render_template, request, redirect
from models import db, Role
from datetime import datetime

role_bp = Blueprint('role', __name__)


@role_bp.route('/roles')
def roles():
    roles = Role.query.filter_by(status='active').all()
    return render_template("roles.html", roles=roles)


@role_bp.route('/add_role')
def add_role_page():
    return render_template("add_role.html")


@role_bp.route('/save_role', methods=['POST'])
def save_role():

    role = Role(
        role_name=request.form['role_name'],
        description=request.form['description'],
        created_at=datetime.utcnow()
    )

    db.session.add(role)
    db.session.commit()

    return redirect('/roles')


@role_bp.route('/delete_role/<int:id>')
def delete_role(id):

    role = Role.query.get(id)
    role.status = 'inactive'

    db.session.commit()

    return redirect('/roles')


@role_bp.route('/edit_role/<int:id>')
def edit_role(id):

    role = Role.query.get(id)

    return render_template("edit_role.html", role=role)


@role_bp.route('/update_role/<int:id>', methods=['POST'])
def update_role(id):

    role = Role.query.get(id)

    role.role_name = request.form['role_name']
    role.description = request.form['description']
    role.updated_at = datetime.utcnow()

    db.session.commit()

    return redirect('/roles')