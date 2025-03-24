import sqlite3

# ✅ Connect to SQLite database
conn = sqlite3.connect("attendance.db", check_same_thread=False)
cursor = conn.cursor()

# ✅ Create the attendance table
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date TEXT,
    status TEXT
)
""")
conn.commit()

# ✅ Function to mark attendance
def mark_attendance(name, date, status):
    cursor.execute("INSERT INTO attendance (name, date, status) VALUES (?, ?, ?)", (name, date, status))
    conn.commit()

# ✅ Function to get all attendance records
def get_attendance():
    cursor.execute("SELECT * FROM attendance")
    return cursor.fetchall()

# ✅ Function to reset attendance
def reset_attendance():
    cursor.execute("DELETE FROM attendance")
    conn.commit()
