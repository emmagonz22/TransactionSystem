from .db import Database
import os
import pandas as pd

# Retrieve environment variables
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")



_db = Database(
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PORT
)

def connect():
    _db.connect() 

def disconnect():
    _db.disconnect()

def get_connection():
    return _db.conn

def get_cursor():
    if _db.conn:
        return _db.conn.cursor()