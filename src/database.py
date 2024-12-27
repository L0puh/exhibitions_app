import sqlite3

from src.common import *

def create_connection() -> sqlite3.Connection:
    try:
        conn = sqlite3.connect(DATABASE_FILE, timeout=10)
        conn.row_factory = sqlite3.Row

    except Error as e:
        print(f"ERROR in connection: {e}")
    return conn


def execute_query(query, data):
    conn = create_connection()
    try:
        conn.cursor().execute(query, data)
        conn.commit()
        conn.close()
    except sqlite3.Error as er:
        print("ERROR:", er)


def create_tables() -> None:
    conn = create_connection()
    with open(SQL_FILE, "r") as f:
        conn.cursor().executescript(f.read())
    conn.commit()
    conn.close()
   
def get_last_id(table, column):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT MAX({column}) FROM {table}")
    result = cursor.fetchone()
    conn.close()
    return result[0] or 0

