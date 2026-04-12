from flask import Blueprint, render_template, request, redirect, session
from models import db, Employee

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
# forget password
# =========================
    
@auth_bp.route('/forget_password')
def forget_password_page():
    return render_template('forget_password.html')    

# =========================
# reset password
# =========================
@auth_bp.route('/reset_password', methods=['POST'])
def reset_password():

    print("RESET FORM:", request.form)

    email = request.form.get('email')
    new_password = request.form.get('new_password')

    user = Employee.query.filter_by(email=email).first()

    if user:
        user.password = new_password
        db.session.commit()
        return redirect('/login')
    else:
        return "User not found"


# =========================
# Logout
# =========================
@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)   # ✅ correct key
    return redirect('/login')