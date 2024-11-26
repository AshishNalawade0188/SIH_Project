import sqlite3

# Connect to SQLite database
db_path = "E:/Project/post.db/sql.db"  # Adjust the path to your SQLite database file
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table for storing snapshots
cursor.execute("""
CREATE TABLE IF NOT EXISTS snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    E:\Project\data\alert TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    people_count INTEGER NOT NULL
);
""")

conn.commit()
conn.close()
print("Snapshots table created successfully.")
