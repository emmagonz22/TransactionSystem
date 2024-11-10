### TODO: This should be remove, this is only here to test automated the population of the db for testing

import psycopg2
import os
from etl import start  # Import the main ETL function from etl.py

db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")
db_name = os.getenv("POSTGRES_DB")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")

def is_database_empty():
    """Check if any table in the database has rows."""
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        cur = conn.cursor()

        # Get a list of all tables in the public schema
        cur.execute("""
            SELECT tablename FROM pg_catalog.pg_tables 
            WHERE schemaname = 'public';
        """)
        tables = cur.fetchall()

        # Check each table for row count
        for table in tables:
            table_name = table[0]
            cur.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = cur.fetchone()[0]
            if row_count > 0:
                print(f"Table '{table_name}' is populated with {row_count} rows.")
                cur.close()
                conn.close()
                return False  # Database is not empty if any table has rows

        # If no table has rows
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Error checking database:", e)
        return False

# Only run ETL if the database is empty
if is_database_empty():
    print("Database is empty. Running ETL process...")
    start()
else:
    print("Database is already populated. Skipping ETL process.")
