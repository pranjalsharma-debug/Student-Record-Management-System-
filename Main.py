
import csv
import json
import os

DATA_FORMAT = "json"
DATA_FOLDER = "data"
DATA_FILE = os.path.join(DATA_FOLDER, f"students.{DATA_FORMAT}")

FIELDS = ["id", "name", "age", "course", "email"]


def setup():
    os.makedirs(DATA_FOLDER, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        save_students([])


def load_students():
    try:
        if not os.path.exists(DATA_FILE):
            return []

        with open(DATA_FILE, "r", newline="", encoding="utf-8") as file:
            if DATA_FORMAT == "json":
                return json.load(file)

            students = []
            reader = csv.DictReader(file)
            for row in reader:
                row["id"] = int(row["id"])
                row["age"] = int(row["age"])
                students.append(row)
            return students

    except (json.JSONDecodeError, csv.Error, ValueError, OSError) as error:
        print("Error loading data:", error)
        return []


def save_students(students):
    try:
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:
            if DATA_FORMAT == "json":
                json.dump(students, file, indent=4)
            else:
                writer = csv.DictWriter(file, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(students)

    except OSError as error:
        print("Error saving data:", error)


def generate_id(students):
    return max([s["id"] for s in students], default=0) + 1


def add_student():
    students = load_students()

    try:
        name = input("Enter name: ").strip()
        age = int(input("Enter age: "))
        course = input("Enter course: ").strip()
        email = input("Enter email: ").strip()

        if not name or not course or not email or age <= 0:
            print("Please enter valid details.")
            return

        student = {
            "id": generate_id(students),
            "name": name,
            "age": age,
            "course": course,
            "email": email
        }

        students.append(student)
        save_students(students)
        print("Student added successfully!")

    except ValueError:
        print("Please enter a valid age.")


def view_students():
    students = load_students()

    if not students:
        print("No student records found.")
        return

    for student in students:
        print(student)


def search_student():
    students = load_students()

    try:
        student_id = int(input("Enter student ID: "))
        student = next(
            (s for s in students if s["id"] == student_id), None
        )

        if student:
            print(student)
        else:
            print("Student not found.")

    except ValueError:
        print("Invalid ID.")


def update_student():
    students = load_students()

    try:
        student_id = int(input("Enter student ID to update: "))
        student = next(
            (s for s in students if s["id"] == student_id), None
        )

        if not student:
            print("Student not found.")
            return

        name = input("Enter new name (or press Enter to skip): ").strip()
        age = input("Enter new age (or press Enter to skip): ").strip()
        course = input("Enter new course (or press Enter to skip): ").strip()
        email = input("Enter new email (or press Enter to skip): ").strip()

        if name:
            student["name"] = name
        if age:
            new_age = int(age)
            if new_age <= 0:
                print("Age must be positive.")
                return
            student["age"] = new_age
        if course:
            student["course"] = course
        if email:
            student["email"] = email

        save_students(students)
        print("Student updated successfully!")

    except ValueError:
        print("Invalid ID or age.")


def delete_student():
    students = load_students()

    try:
        student_id = int(input("Enter student ID to delete: "))
        updated = [s for s in students if s["id"] != student_id]

        if len(updated) == len(students):
            print("Student not found.")
            return

        save_students(updated)
        print("Student deleted successfully!")

    except ValueError:
        print("Invalid ID.")


def sort_students():
    students = load_students()
    sorted_students = sorted(
        students, key=lambda s: s["name"].lower()
    )

    for student in sorted_students:
        print(student)


def filter_students():
    students = load_students()
    course = input("Enter course: ").strip().lower()

    filtered = [
        s for s in students
        if s["course"].lower() == course
    ]

    for student in filtered:
        print(student)

    if not filtered:
        print("No matching students found.")


def main():
    setup()

    while True:
        print("\nSTUDENT RECORD MANAGEMENT SYSTEM")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Sort Students")
        print("7. Filter by Course")
        print("8. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                add_student()
            elif choice == "2":
                view_students()
            elif choice == "3":
                search_student()
            elif choice == "4":
                update_student()
            elif choice == "5":
                delete_student()
            elif choice == "6":
                sort_students()
            elif choice == "7":
                filter_students()
            elif choice == "8":
                print("Thank you!")
                break
            else:
                print("Invalid choice.")

        except Exception as error:
            print("An unexpected error occurred:", error)

        finally:
            print("Operation completed.")


if __name__ == "__main__":
    main()
      
