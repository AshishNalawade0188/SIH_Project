import sqlite3
import pandas as pd

# Define the database file path
db_file = r"E:\Project\post.db\sql.db"  # Update with your actual database path

# Connect to the SQLite database
conn = sqlite3.connect(db_file)

# Step 1: Check if the table exists
table_name = 'Citizen_Centric_Services'  # Replace with your actual table name
query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
cursor = conn.cursor()
cursor.execute(query)
table_exists = cursor.fetchone()

if table_exists:
    print(f"Table '{table_name}' exists in the database.")
    
    # Step 2: Retrieve and display the first 5 rows from the table
    query = f"SELECT * FROM {table_name} LIMIT 5;"
    data = pd.read_sql_query(query, conn)
    print("First 5 rows of data:")
    print(data)
else:
    print(f"Table '{table_name}' does not exist in the database.")

# Close the connection
conn.close()