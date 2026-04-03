from flask import Flask
from models import db

from routes.department_routes import department_bp
from routes.employee_routes import employee_bp
from routes.attendance_routes import attendance_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hrm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(department_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(attendance_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)