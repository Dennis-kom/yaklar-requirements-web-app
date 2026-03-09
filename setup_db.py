#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, 'C:\\repositories\\yaklar-requirements-web-app')

from requests_application.app import create_app, db
import sqlite3

print("Starting database setup...")

# Create app
app = create_app()
print("App created")

# Ensure instance directory exists
os.makedirs('C:\\repositories\\yaklar-requirements-web-app\\instance', exist_ok=True)
print("Instance directory ready")

# Create database
with app.app_context():
    db.create_all()
    print("Database tables created")

    # Check schema
    db_path = 'C:\\repositories\\yaklar-requirements-web-app\\instance\\appdata.db'
    if os.path.exists(db_path):
        print(f"Database file exists: {db_path}")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(cit_request)")
        columns = cursor.fetchall()
        print("Columns in cit_request table:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        col_names = [col[1] for col in columns]
        if 'location' in col_names:
            print("\nSUCCESS: location column exists!")
        else:
            print("\nERROR: location column missing!")
        conn.close()
    else:
        print(f"ERROR: Database file not found at {db_path}")

