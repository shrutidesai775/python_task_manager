import sqlite3

def connect_db():
    return sqlite3.connect("data.db")

def add_task():
    task = input("Enter task name: ")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (task_name) VALUES (?)",
        (task,)
    )

    conn.commit()
    conn.close()

    print("Task added successfully!")

def view_tasks():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    print("\n--- Your Tasks ---")

    for task in tasks:
        print(task[0], "-", task[1])

    conn.close()

def delete_task():
    view_tasks()

    task_id = input("Enter task ID to delete: ")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    if cursor.rowcount > 0:
        print("Task deleted successfully!")
    else:
        print("Task ID not found!")

    conn.commit()
    conn.close()    

def main():
    while True:
        print("\n1. Add Task")
        print("2. View Tasks")
        print("3. delete task")
        print("4.Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            delete_task()
        elif choice == "4":
            print("Thank you!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()