"""
Description : A menu-driven CLI app to Add / View / Update /
              Delete student records stored in a JSON file.
Modules Used: json, os, re
"""

import json
import os
import re

DATA_FILE = "students.json"

def load_students():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("\n  [ERROR] Corrupted JSON file. Resetting data.\n")
        return []

def save_students(students):
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=4)

def is_valid_age(age):
    return age.isdigit() and 1 <= int(age) <= 120

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def find_student(students, roll):
    for i, s in enumerate(students):
        if s["roll"].lower() == roll.lower():
            return i, s
    return -1, None

def print_table(students):
    if not students:
        print("\n  [INFO] No records found.\n")
        return

    print("\n" + "  " + "═" * 65)
    print(f"  {'Roll':<10} {'Name':<20} {'Age':<5} {'Grade':<8} {'Email'}")
    print("  " + "─" * 65)

    for s in students:
        print(f"  {s['roll']:<10} {s['name']:<20} {s['age']:<5} {s['grade']:<8} {s['email']}")

    print("  " + "═" * 65 + "\n")

def add_student(students):
    print("\n  ── Add Student ──")

    roll = input("  Roll No : ").strip()
    _, existing = find_student(students, roll)
    if existing:
        print("  [ERROR] Roll already exists.\n")
        return

    name = input("  Name    : ").strip()

    while True:
        age = input("  Age     : ").strip()
        if is_valid_age(age):
            break
        print("  [!] Enter valid age (1–120)")

    grade = input("  Grade   : ").strip()

    while True:
        email = input("  Email   : ").strip()
        if is_valid_email(email):
            break
        print("  [!] Invalid email format")

    students.append({
        "roll": roll,
        "name": name,
        "age": age,
        "grade": grade,
        "email": email
    })

    save_students(students)
    print(f"\n  ✔ Student '{name}' added.\n")

def view_all_students(students):
    print("\n  ── All Students ──")
    print_table(students)

def search_student(students):
    roll = input("\n  Enter Roll No: ").strip()
    _, student = find_student(students, roll)

    if student:
        print_table([student])
    else:
        print("  [NOT FOUND]\n")

def update_student(students):
    roll = input("\n  Enter Roll No to update: ").strip()
    idx, student = find_student(students, roll)

    if not student:
        print("  [NOT FOUND]\n")
        return

    print("\n  Press Enter to keep old value\n")

    name = input(f"  Name [{student['name']}]: ").strip() or student["name"]

    while True:
        age = input(f"  Age [{student['age']}]: ").strip()
        if not age:
            age = student["age"]
            break
        if is_valid_age(age):
            break
        print("  [!] Invalid age")

    grade = input(f"  Grade [{student['grade']}]: ").strip() or student["grade"]

    while True:
        email = input(f"  Email [{student['email']}]: ").strip()
        if not email:
            email = student["email"]
            break
        if is_valid_email(email):
            break
        print("  [!] Invalid email")

    students[idx] = {
        "roll": roll,
        "name": name,
        "age": age,
        "grade": grade,
        "email": email
    }

    save_students(students)
    print("\n  ✔ Updated successfully.\n")

def delete_student(students):
    roll = input("\n  Enter Roll No to delete: ").strip()
    idx, student = find_student(students, roll)

    if not student:
        print("  [NOT FOUND]\n")
        return

    confirm = input(f"  Delete {student['name']}? (yes/no): ").lower()
    if confirm == "yes":
        students.pop(idx)
        save_students(students)
        print("  ✔ Deleted\n")
    else:
        print("  Cancelled\n")

def main():
    print("=" * 50)
    print("     Synent Technologies – Student Management")
    print("=" * 50)

    while True:
        print("\n" + "=" * 50)
        print("                MAIN MENU")
        print("=" * 50)
        print("  1. Add Student")
        print("  2. View All Students")
        print("  3. Search Student")
        print("  4. Update Student")
        print("  5. Delete Student")
        print("  6. Exit")
        print("=" * 50)

        choice = input("\n  Enter your choice (1-6): ").strip()
        students = load_students()

        if choice == "1":
            print("\n" + "=" * 50)
            print("                ADD STUDENT")
            print("=" * 50)
            add_student(students)

        elif choice == "2":
            print("\n" + "=" * 50)
            print("             VIEW ALL STUDENTS")
            print("=" * 50)
            view_all_students(students)

        elif choice == "3":
            print("\n" + "=" * 50)
            print("              SEARCH STUDENT")
            print("=" * 50)
            search_student(students)

        elif choice == "4":
            print("\n" + "=" * 50)
            print("              UPDATE STUDENT")
            print("=" * 50)
            update_student(students)

        elif choice == "5":
            print("\n" + "=" * 50)
            print("              DELETE STUDENT")
            print("=" * 50)
            delete_student(students)

        elif choice == "6":
            print("\n" + "=" * 50)
            print("                  GOODBYE")
            print("=" * 50 + "\n")
            break

        else:
            print("\n  [!] Invalid choice. Try again.\n")

            students = load_students()
            save_students(students)

if __name__ == "__main__":
    main()