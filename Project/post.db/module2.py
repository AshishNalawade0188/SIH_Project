import sqlite3
import pandas as pd
import os

# Define the path to your SQLite database (it will be created if it doesn't exist)
db_file = r"E:\Project\post.db\sql.db" # Change the path if necessary

# List of CSV file paths you want to import
csv_files = [
    r"E:\Project\post.db\mail.csv",  # Replace with actual CSV file paths
    r"E:\Project\post.db\Saving Bank.csv",
    r"E:\Project\post.db\Payment Bank.csv",
    r"post.db/Citizen Centric Services.csv",
    r"E:\Project\post.db\Insurance.csv",
    r"E:\Project\feedback\feedback.csv"
]

# Connect to SQLite database (it will create it if it doesn't exist)
conn = sqlite3.connect(db_file)

# Function to load a CSV into a table in SQLite
def load_csv_to_db(csv_file, conn):
    try:
        # Read the CSV file into a Pandas DataFrame
        data = pd.read_csv(csv_file)
        
        # Generate table name based on the CSV file name (without the .csv extension)
        table_name = os.path.basename(csv_file).replace('.csv', '').replace(' ', '_')
        
        # Load data into SQLite database, creating a new table with the columns from the CSV file
        data.to_sql(table_name, conn, if_exists='replace', index=False)
        
        print(f"Data from {csv_file} has been successfully added to the table '{table_name}' in the database.")
    except Exception as e:
        print(f"Error occurred while loading {csv_file}: {e}")

# Loop through each CSV file and load data into the database
for csv_file in csv_files:
    load_csv_to_db(csv_file, conn)  # Load data into the database

# Close the database connection after all CSVs are loaded
conn.close()

print("All CSV files have been loaded successfully.")