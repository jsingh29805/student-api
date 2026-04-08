from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Create DB + table
def init_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# GET all students
@app.route('/students', methods=['GET'])
def get_students():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    conn.close()

    students = [{"id": row[0], "name": row[1]} for row in data]
    return jsonify(students), 200

# POST new student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()

    if not data or "name" not in data:
        return {"error": "Invalid input"}, 400

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name) VALUES (?)", (data["name"],))
    conn.commit()
    conn.close()

    return {"message": "Student added"}, 201

# PUT update student
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()

    if not student:
        return {"error": "Student not found"}, 404

    cursor.execute("UPDATE students SET name=? WHERE id=?", (data["name"], id))
    conn.commit()
    conn.close()

    return {"message": "Student updated"}, 200

# DELETE student
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()

    if not student:
        return {"error": "Student not found"}, 404

    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return {"message": "Student deleted"}, 200
@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()
    conn.close()

    if not student:
        return {"error": "Student not found"}, 404

    return jsonify({"id": student[0], "name": student[1]}), 200
@app.route('/search', methods=['GET'])
def search_student():
    name = request.args.get('name')

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + name + '%',))
    results = cursor.fetchall()
    conn.close()

    students = [{"id": r[0], "name": r[1]} for r in results]

    return jsonify(students), 200

if __name__ == '__main__':
    app.run(debug=True)