import sqlite3


def connect_db():
    return sqlite3.connect("data.db")


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


def add_record():
    name = input("Enter name: ").strip()
    email = input("Enter email: ").strip().lower()

    # Validate empty inputs
    if not name or not email:
        print("Error: Name and email cannot be empty.")
        return

    # Basic email validation
    if "@" not in email or "." not in email.split("@")[-1]:
        print("Error: Please enter a valid email.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    # Check for duplicate name or email
    cursor.execute(
        "SELECT id FROM records WHERE name = ? OR email = ?",
        (name, email)
    )

    existing = cursor.fetchone()

    if existing:
        print("Classification: REDUNDANT DATA")
        print("Duplicate record detected! Data was not added.")
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

    cursor.execute("SELECT * FROM records")
    records = cursor.fetchall()

    if records:
        print("\n--- Stored Records ---")

        for record in records:
            print(record)
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
