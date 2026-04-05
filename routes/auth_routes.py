from flask import Blueprint, render_template, request, redirect, session
from models import Employee

auth_bp = Blueprint('auth', __name__)


# =========================
# Login Page
# =========================
@auth_bp.route('/login')
def login_page():
    return render_template("login.html")


# =========================
# Login Logic
# =========================
@auth_bp.route('/login_user', methods=['POST'])
def login_user():

    email = request.form['username']   # form field stays "username"
    password = request.form['password']

    user = Employee.query.filter_by(email=email).first()

    if user and user.password == password:
        session['user_id'] = user.emp_id
        return redirect('/dashboard')
    else:
        return "Invalid Login"


# =========================
# Logout
# =========================
@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)   # ✅ correct key
    return redirect('/login')