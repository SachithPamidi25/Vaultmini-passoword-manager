import mysql.connector

conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_mysql_password",  # CHANGE THIS
    database="vaultmini"
)

cursor=conn.cursor(dictionary=True)