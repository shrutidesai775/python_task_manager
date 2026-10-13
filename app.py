import sqlite3
import re


DATABASE = "data.db"


def connect_db():
    return sqlite3.connect(DATABASE)


def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)

    conn.commit()
    conn.close()


def is_valid_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None


def add_record():
    name = input("Enter name: ").strip()
    email = input("Enter email: ").strip().lower()

    # Validate input
    if not name or not email:
        print("Error: Name and email cannot be empty.")
        return

    if not is_valid_email(email):
        print("Error: Please enter a valid email.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    # Check for an existing email first
    cursor.execute(
        "SELECT id, name, email FROM records WHERE email = ?",
        (email,)
    )
    existing_email = cursor.fetchone()

    if existing_email:
        print("Classification: REDUNDANT DATA")
        print("This email already exists. Record was not added.")
        conn.close()
        return

    # Check whether the name already exists
    cursor.execute(
        "SELECT id, name, email FROM records WHERE name = ?",
        (name,)
    )
    existing_name = cursor.fetchone()

    if existing_name:
        print("Possible duplicate detected: same name.")

        confirm = input(
            "Is this a different person? (yes/no): "
        ).strip().lower()

        if confirm == "yes":
            cursor.execute(
                "INSERT INTO records (name, email) VALUES (?, ?)",
                (name, email)
            )
            conn.commit()

            print("Classification: FALSE POSITIVE")
            print("Record added after user confirmation.")

        else:
            print("Classification: REDUNDANT DATA")
            print("Record was not added.")

    else:
        cursor.execute(
            "INSERT INTO records (name, email) VALUES (?, ?)",
            (name, email)
        )
        conn.commit()

        print("Classification: UNIQUE DATA")
        print("Unique record added successfully!")

    conn.close()


def view_records():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email FROM records")
    records = cursor.fetchall()

    if records:
        print("\n--- Stored Records ---")

        for record in records:
            print(
                f"ID: {record[0]} | "
                f"Name: {record[1]} | "
                f"Email: {record[2]}"
            )
    else:
        print("No records found.")

    conn.close()


def main():
    create_table()

    while True:
        print("\n--- Data Redundancy Removal System ---")
        print("1. Add record")
        print("2. View records")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_record()

        elif choice == "2":
            view_records()

        elif choice == "3":
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
