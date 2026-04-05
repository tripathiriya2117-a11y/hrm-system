from flask import Blueprint, render_template, request, redirect, session
from models import db, Employee

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login')
def login_page():
    return render_template("login.html")


@auth_bp.route('/login_user', methods=['POST'])
def login_user():

    username = request.form['username']
    password = request.form['password']

    user = Employee.query.filter_by(
        username=username,
        password=password
    ).first()

    if user:
        return redirect('/employees')
    else:
        return "Invalid Login"


@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

