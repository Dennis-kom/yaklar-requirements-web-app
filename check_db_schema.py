import sqlite3
import os

db_path = "C:\\repositories\\yaklar-requirements-web-app\\instance\\appdata.db"

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(cit_request)")
    columns = cursor.fetchall()
    print("Columns in cit_request table:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    conn.close()
    print("\nDatabase schema is correct!")
else:
    print(f"Database file not found at {db_path}")

