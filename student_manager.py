import sqlite3

# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create the students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    grade TEXT NOT NULL,
    email TEXT NOT NULL
)
""")
conn.commit()

def add_student():
    try:
        id = int(input("Enter student ID: "))
        name = input("Enter student name: ")
        grade = input("Enter student grade: ")
        email = input("Enter student email: ")
        if "@" not in email:
            raise ValueError("Invalid email address")
        cursor.execute("INSERT INTO students (id, name, grade, email) VALUES (?, ?, ?, ?)",
                       (id, name, grade, email))
        conn.commit()
        print("Student added successfully.")
    except Exception as e:
        print(f"Error: {e}")

def view_students():
    try:
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("No records found.")
    except Exception as e:
        print(f"Error: {e}")

def update_student():
    try:
        id = int(input("Enter student ID to update: "))
        cursor.execute("SELECT * FROM students WHERE id = ?", (id,))
        student = cursor.fetchone()
        if not student:
            print("Student not found.")
            return

        current_name, current_grade, current_email = student[1], student[2], student[3]

        name = input(f"Enter new name (Leave blank to keep '{current_name}'): ") or current_name
        grade = input(f"Enter new grade (Leave blank to keep '{current_grade}'): ") or current_grade
        email = input(f"Enter new email (Leave blank to keep '{current_email}'): ") or current_email

        if "@" not in email:
            raise ValueError("Invalid email address")

        cursor.execute("UPDATE students SET name = ?, grade = ?, email = ? WHERE id = ?",
                       (name, grade, email, id))
        conn.commit()
        print("Student updated successfully.")
    except Exception as e:
        print(f"Error: {e}")

def delete_student():
    try:
        id = int(input("Enter student ID to delete: "))
        confirm = input("Are you sure you want to delete this student? (y/n): ").lower()
        if confirm == 'y':
            cursor.execute("DELETE FROM students WHERE id = ?", (id,))
            conn.commit()
            print("Student deleted successfully.")
        else:
            print("Deletion cancelled.")
    except Exception as e:
        print(f"Error: {e}")

def menu():
    while True:
        print("\nStudent Record Management")
        print("1. Add Student")
        print("2. View Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            update_student()
        elif choice == '4':
            delete_student()
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

menu()
conn.close()
