import os

def icon(path:str):
    return os.path.join(ICON_DIR, path)

ICON_DIR = os.path.join(os.getcwd(), 'assets', 'icons')
SQL_FILE = os.path.join(os.getcwd(), 'assets', 'query.sql')
DATABASE_FILE = os.path.join(os.getcwd(), 'assets', 'database.db')




