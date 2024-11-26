import sqlite3

# Connect to SQLite database
db_path = "E:\Project\post.db\sql.db"  # Replace with your database name
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# File path to insert into the table
file_path = "data/alerts/alert_frame_418.jpg"  # Replace with the actual file path

try:
    # Insert the file path into the snapshot table
    cursor.execute("""
        INSERT INTO snapshot (file_path)
        VALUES (?)
    """, (file_path,))
    
    # Commit the transaction
    conn.commit()
    print(f"File path '{file_path}' inserted successfully into the 'snapshot' table.")
except sqlite3.Error as e:
    print("Error occurred while inserting file path:", e)
finally:
    # Close the database connection
    conn.close()


    