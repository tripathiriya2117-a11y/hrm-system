from flask import Flask
from models import db

# import blueprints
from routes.department_routes import department_bp
from routes.employee_routes import employee_bp
from routes.attendance_routes import attendance_bp

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hrm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize database
db.init_app(app)

# register route modules
app.register_blueprint(department_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(attendance_bp)

# create tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)