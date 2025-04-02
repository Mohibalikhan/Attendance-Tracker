import sqlite3

# ✅ Connect to SQLite database
conn = sqlite3.connect("attendance.db", check_same_thread=False)
cursor = conn.cursor()

# ✅ Drop existing table (ONLY for development)
cursor.execute("DROP TABLE IF EXISTS attendance")

# ✅ Create the attendance table (with Roll No)
cursor.execute("""
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT,  -- ✅ Added Roll No
    name TEXT,
    date TEXT,
    status TEXT
)
""")
conn.commit()

# ✅ Function to mark attendance
def mark_attendance(roll_no, name, date, status):
    cursor.execute("INSERT INTO attendance (roll_no, name, date, status) VALUES (?, ?, ?, ?)", 
                   (roll_no, name, date, status))
    conn.commit()

# ✅ Function to get all attendance records
def get_attendance():
    cursor.execute("SELECT roll_no, name, date, status FROM attendance")  # ✅ Fetch roll numbers too
    return cursor.fetchall()

# ✅ Function to reset attendance
def reset_attendance():
    cursor.execute("DELETE FROM attendance")
    conn.commit()
