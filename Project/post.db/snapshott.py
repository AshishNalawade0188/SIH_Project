import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
db_path = "E:\Project\post.db\sql.db"  # Replace with the desired database name
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create a table with a single column for storing file paths
try:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS snapshot (
            file_path TEXT NOT NULL
        )
    """)
    conn.commit()
    print("Table 'snapshot' created successfully.")
except sqlite3.Error as e:
    print("Error occurred while creating the table:", e)
finally:
    # Close the database connection
    conn.close()
