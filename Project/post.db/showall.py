import sqlite3

# Define the path to your SQLite database
db_file = r"E:\Project\post.db\sql.db"  # Change to your actual database path

# Connect to the SQLite database
conn = sqlite3.connect(db_file)

# Create a cursor object
cursor = conn.cursor()

# Query to get all table names in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Fetch all the table names
tables = cursor.fetchall()

# Print all table names
print("Tables in the database:")
for table in tables:
    print(table[0])

# Close the connection
conn.close()