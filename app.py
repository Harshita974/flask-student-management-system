import os from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from functools import wraps

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' not in session or session.get('role') != 'admin':
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return wrapper

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
# Automatically create the 'users' table if it doesn't exist
with sqlite3.connect("database.db") as conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        
        db = get_db()
        try:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Username already exists! Please try a different one."
        except Exception as e:
            return f"An error occurred: {e}"
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        
        if user and check_password_hash(user['password'], password):
            session['user'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
            
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login')) # If not logged in, send them back to login [cite: 102, 103]
    return render_template('dashboard.html', user=session['user']) # Show user's name on dashboard [cite: 104]

@app.route('/logout')
def logout():
    session.pop('user', None) # Remove the user from the "session" 
    return redirect(url_for('login')) # Send them back to login page [cite: 108]

@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    # Only logged-in users can access this [cite: 95-96, 176-177]
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        # Get data from the HTML form [cite: 98-101]
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']

        # Save to the students table [cite: 102-106]
        db = get_db()
        db.execute("INSERT INTO students (name, email, course) VALUES (?, ?, ?)", (name, email, course))
        db.commit()
        
        # After saving, go to the students list page [cite: 107]
        return redirect('/students')

    return render_template('add_student.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    # Security Check [cite: 123-124, 176]
    if 'user' not in session:
        return redirect('/login')

    db = get_db()
    
    # 1. Fetch the existing data for this specific student [cite: 126-128]
    student = db.execute("SELECT * FROM students WHERE id = ?", (id,)).fetchone()

    if request.method == 'POST':
        # 2. Get the updated information from the form [cite: 132-134]
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']

        # 3. Run the UPDATE command in the database [cite: 130-138]
        db.execute("UPDATE students SET name=?, email=?, course=? WHERE id=?", 
                   (name, email, course, id))
        db.commit()
        
        # 4. Go back to the list to see the changes [cite: 139]
        return redirect('/students')

    return render_template('edit_student.html', student=student)

@app.route('/delete/<int:id>')
def delete_student(id):
    # Security Check [cite: 145-146, 176]
    if 'user' not in session:
        return redirect('/login')

    db = get_db()
    # Remove the student record using their unique ID [cite: 148-149]
    db.execute("DELETE FROM students WHERE id=?", (id,))
    db.commit()
    
    return redirect('/students')

@app.route('/students')
def students():
    if 'user' not in session:
        return redirect('/login')
    db = get_db()
    data = db.execute("SELECT * FROM students").fetchall()
    return render_template('students.html', students=data)

@app.route('/admin')
@admin_required
def admin_dashboard():
    db = get_db()
    users = db.execute("SELECT id, username, role FROM users").fetchall()
    return render_template('admin.html', users=users)

@app.route('/api/students', methods=['GET'])
def api_get_students():
    db = get_db()
    students = db.execute("SELECT * FROM students").fetchall()
    return jsonify([dict(row) for row in students])

@app.route('/api/students', methods=['POST'])
def api_add_student():
    data = request.get_json()
    db = get_db()
    db.execute(
        "INSERT INTO students (name, email, course) VALUES (?, ?, ?)",
        (data['name'], data['email'], data['course'])
    )
    db.commit()
    return jsonify({"message": "Student added successfully"})

@app.route('/api/students/<int:id>', methods=['PUT'])
def api_update_student(id):
    data = request.get_json()
    db = get_db()
    db.execute(
        "UPDATE students SET name=?, email=?, course=? WHERE id=?",
        (data['name'], data['email'], data['course'], id)
    )
    db.commit()
    return jsonify({"message": "Student updated"})

if __name__ == '__main__':
    app.run(debug=False) # Start the server [cite: 110]





