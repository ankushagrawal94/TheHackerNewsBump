import MySQLdb
import time
import re
import datetime

start_time = time.time()
elapsed_time = time.time()

db = MySQLdb.connect(host="localhost", # your host, usually localhost
	                     user="root", # your username
	                      passwd="password", # your password
	                      db="githubDB") # name of the data base

cur = db.cursor() 
cursor.execute("DROP TABLE IF EXISTS event_table_condensed")
cur.execute("""CREATE TABLE event_table_condensed( repo_name VARCHAR(255), stars INT(6), event_time DATE ) """)
db.commit()


