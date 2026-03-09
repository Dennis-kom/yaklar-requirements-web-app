import sqlite3
import os

db_path = "C:\\repositories\\yaklar-requirements-web-app\\instance\\appdata.db"

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(cit_request)")
    columns = cursor.fetchall()
    print("All columns in cit_request table:")
    for col in columns:
        print(f"{col[1]} - {col[2]}")

    # Check if location column exists
    col_names = [col[1] for col in columns]
    if 'location' in col_names:
        print("\n✓ location column EXISTS")
    else:
        print("\n✗ location column MISSING")

    conn.close()
else:
    print(f"Database file not found at {db_path}")

