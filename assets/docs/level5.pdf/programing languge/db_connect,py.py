import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name=None):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=127.0.0.1,
            user=h,
            passwd=H.s.s123,
            database=db_name
        )
