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

    print("FORM:", request.form)
    print("DB:", [(u.email, u.password) for u in Employee.query.all()])

    user = Employee.query.filter_by(
        email=request.form['username'],
        password=request.form['password']
    ).first()

    if user:
        session['user_id'] = user.emp_id
        return redirect('/dashboard')
    else:
        return "Invalid Login"

# =========================
# froget password
# =========================
    
@auth_bp.route('/forget_password')
def forget_password_page():
    return render_template('forget_password.html')    

# =========================
# Logout
# =========================
@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)   # ✅ correct key
    return redirect('/login')