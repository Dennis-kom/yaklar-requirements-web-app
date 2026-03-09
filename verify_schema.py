import sqlite3

conn = sqlite3.connect(r'C:\repositories\yaklar-requirements-web-app\instance\appdata.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(cit_request)")
columns = cursor.fetchall()

print("Columns in cit_request table:")
for col in columns:
    print(f"{col[1]} - {col[2]}")

col_names = [col[1] for col in columns]
if 'location' in col_names:
    print("\nSUCCESS: location column found!")
else:
    print("\nERROR: location column NOT found!")
    print(f"Available columns: {col_names}")

conn.close()

