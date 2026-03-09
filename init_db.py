from requests_application.app import create_app, db
import os

app = create_app()

# Ensure instance directory exists
os.makedirs('instance', exist_ok=True)

with app.app_context():
    try:
        db.create_all()
        print("Database tables created successfully!")

        # Verify the schema
        import sqlite3
        conn = sqlite3.connect('instance/appdata.db')
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(cit_request)")
        columns = cursor.fetchall()
        col_names = [col[1] for col in columns]

        print(f"Created columns: {', '.join(col_names)}")

        if 'location' in col_names:
            print("OK: Location column exists!")
        else:
            print("WARNING: Location column not found!")

        conn.close()
    except Exception as e:
        print(f"ERROR creating database: {e}")



