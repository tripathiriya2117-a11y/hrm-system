from flask import Flask
from models import db
import os

app = Flask(__name__)


app.secret_key = "secret123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hrm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# 🔥 IMPORT AFTER app created
from routes.department_routes import department_bp
from routes.employee_routes import employee_bp
from routes.attendance_routes import attendance_bp
from routes.role_routes import role_bp
from routes.auth_routes import auth_bp
from routes.task_routes import task_bp


app.register_blueprint(department_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(role_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(task_bp)


with app.app_context():
    db.create_all()

from flask import session, redirect

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect('/dashboard')
    else:
        return redirect('/login')

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000  
    )

