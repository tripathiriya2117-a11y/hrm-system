from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root1234",   # your mysql password
    database="hrm_db"
)

cursor = db.cursor()

@app.route('/')
def index():

    search = request.args.get('search')

    if search:
        query = "SELECT * FROM department WHERE dept_name LIKE %s AND status='active'"
        cursor.execute(query,('%'+search+'%',))
    else:
        query = "SELECT * FROM department WHERE status='active'"
        cursor.execute(query)

    departments = cursor.fetchall()

    return render_template("index.html", departments=departments)
    cursor.execute("SELECT * FROM department WHERE status='active'")
    departments = cursor.fetchall()
    return render_template("index.html", departments=departments)


@app.route('/add_department', methods=['POST'])
def add_department():
    dept_name = request.form['dept_name']
    description = request.form['description']

    query = "INSERT INTO department (dept_name, description) VALUES (%s,%s)"
    cursor.execute(query,(dept_name,description))
    db.commit()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete_department(id):
    query = "UPDATE department SET status='inactive' WHERE dept_id=%s"
    cursor.execute(query,(id,))
    db.commit()

    return redirect('/')

@app.route('/edit/<int:id>')
def edit_department(id):

    query = "SELECT * FROM department WHERE dept_id=%s"
    cursor.execute(query,(id,))
    department = cursor.fetchone()

    return render_template("edit_department.html", dept=department)

@app.route('/update/<int:id>', methods=['POST'])
def update_department(id):

    dept_name = request.form['dept_name']
    description = request.form['description']

    query = "UPDATE department SET dept_name=%s, description=%s WHERE dept_id=%s"

    cursor.execute(query,(dept_name,description,id))
    db.commit()

    return redirect('/')

@app.route('/add')
def add_page():
    return render_template("add_department.html")


if __name__ == "__main__":
    app.run(debug=True)