import sqlite3

from src.common import *

def create_connection() -> sqlite3.Connection:
    try:
        conn = sqlite3.connect(DATABASE_FILE, timeout=10)
        conn.row_factory = sqlite3.Row

    except Error as e:
        print(f"ERROR in connection: {e}")
    return conn


def execute_query(query, data=None):
    conn = create_connection()
    try:
        if data:
            conn.cursor().execute(query, data)
        else:
            conn.cursor().execute(query)
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

def select_all(table) -> list:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    data = []
    for row in rows:
        data.append(row)

    return data


def select_where(table, key, value) -> list:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table} WHERE {key} = {value}")
    rows = cursor.fetchall()
    data = []
    for row in rows:
        data.append(row)

    return data

def select_one_where(table, keys:list, values:list) -> sqlite3.Row :
    conn = create_connection()
    cursor = conn.cursor()
    query = f"SELECT * FROM {table} WHERE"
    for i, key in enumerate(keys):
        query += f" {key} = {values[i]} AND"
    cursor.execute(query[:-3])
    rows = cursor.fetchone()
    return rows

def delete_where(table, key, value):
    query = f"DELETE FROM {table} WHERE {key} = {value};"
    execute_query(query)
