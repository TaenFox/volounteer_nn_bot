import mysql.connector
import config
from mysql.connector import errorcode

db_base=config.db_base

config = {
  'host':'localhost',
  'user': config.db_log,
  'password': config.db_pass,
  'database': 'test',
  'client_flags': [mysql.connector.ClientFlag.SSL],
# 'ssl_ca': '<path-to-SSL-cert>/DigiCertGlobalRootG2.crt.pem'
}

try:
   conn = mysql.connector.connect(**config)
   print("Connection established")
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with the user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cursor = conn.cursor()

def select(expression):
  cursor.execute(expression)
  return cursor.fetchall()

def db_test_query(apple):
    cursor.execute(f"insert into apples (`apple`) values ('{apple}');")
    # print("Inserted",cursor.rowcount,"row(s) of data.")
    print(cursor.lastrowid)
    conn.commit()