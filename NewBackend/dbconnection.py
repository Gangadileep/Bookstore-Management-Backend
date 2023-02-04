import pymysql
from config import mydb

def connect_and_commit(query, data=None):
    conn = mydb.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query, data)
    conn.commit()
    cursor.close()
    conn.close()
