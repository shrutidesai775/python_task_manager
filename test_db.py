import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name TEXT NOT NULL
)
""")

cursor.execute(
    "INSERT INTO tasks (task_name) VALUES (?)",
    ("Learn Python",)
)

conn.commit()

cursor.execute("SELECT * FROM tasks")
rows = cursor.fetchall()

print("Tasks saved in database:")
for row in rows:
    print(row)

conn.close()