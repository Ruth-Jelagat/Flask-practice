from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ----------------------
# Initialize DB
# ----------------------
def init_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            course TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ----------------------
# Home - View All Students
# ----------------------
@app.route('/')
def index():
    search = request.args.get('search')  # ?search=Ruth
    sort = request.args.get('sort')      # ?sort=age or ?sort=course
    
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    query = "SELECT * FROM students"
    params = []
    
    # Search
    if search:
        query += " WHERE name LIKE ?"
        params.append(f"%{search}%")
    
    # Sort
    if sort in ['name', 'age', 'course']:
        query += f" ORDER BY {sort}"
    
    cursor.execute(query, params)
    students = cursor.fetchall()
    conn.close()
    return render_template('index.html', students=students, search=search, sort=sort)

# ----------------------
# Add Student
# ----------------------
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']

        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
                       (name, age, course))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add.html')

# ----------------------
# Edit Student
# ----------------------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']
        cursor.execute("UPDATE students SET name=?, age=?, course=? WHERE id=?",
                       (name, age, course, id))
        conn.commit()
        conn.close()
        return redirect('/')
    
    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()
    conn.close()
    return render_template('edit.html', student=student)

# ----------------------
# Delete Student
# ----------------------
@app.route('/delete/<int:id>')
def delete_student(id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/about')
def about():
    return "About Page"

@app.route('/contact')
def contact():
    return "Contact Us"

# ----------------------
# Run App
# ----------------------
if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000)
