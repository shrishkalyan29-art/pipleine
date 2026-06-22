import csv
import sqlite3

# Define file paths and database names
CSV_FILE = 'source_data.csv'
DB_FILE = 'my_database.db'

def run_pipeline():
    print("Initializing pipeline...")
    
    # ----------------------------------------------------
    # 1. EXTRACT: Read data from the Flat File (CSV)
    # ----------------------------------------------------
    extracted_data = []
    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            extracted_data.append(row)
            
    print(print(f"Extracted {len(extracted_data)} records."))

    # ----------------------------------------------------
    # 2. TRANSFORM: Clean and standardize the data
    # ----------------------------------------------------
    transformed_data = []
    for row in extracted_data:
        # Standardize names: remove accidental spaces and capitalize nicely
        clean_name = row['name'].strip().title()
        
        # Standardize emails: make everything lowercase
        clean_email = row['email'].strip().lower()
        
        # Keep ID and date as they are
        record_id = int(row['id'])
        signup_date = row['signup_date']
        
        # Store the cleaned record as a tuple (perfect for SQL insertion)
        transformed_data.append((record_id, clean_name, clean_email, signup_date))
        
    print("Data transformation complete.")

    # ----------------------------------------------------
    # 3. LOAD: Insert the data into the RDBMS (SQLite)
    # ----------------------------------------------------
    # Connect to SQLite (creates the database file if it doesn't exist)
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    
    # Create a table to hold our data if it doesn't already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            signup_date TEXT
        )
    ''')
    
    # Insert the transformed data into the table
    # The '?' placeholders prevent security bugs (SQL injection)
    cursor.executemany('''
        INSERT OR REPLACE INTO users (id, name, email, signup_date)
        VALUES (?, ?, ?, ?)
    ''', transformed_data)
    
    # Commit (save) the changes and close the connection
    connection.commit()
    connection.close()
    
    print("Data successfully loaded into the database!")

# Run the pipeline
if __name__ == "__main__":
    run_pipeline()