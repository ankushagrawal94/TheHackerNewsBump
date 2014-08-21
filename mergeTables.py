import MySQLdb
import time
import re
import datetime

db = MySQLdb.connect(host="localhost", # your host, usually localhost
	                     user="root", # your username
	                      passwd="password", # your password
	                      db="githubDB") # name of the data base

cur = db.cursor() 

cur.execute("select * from event_table_general_condensed2")

all_data = cur.fetchall()

for event in all_data:
	cur.execute("INSERT INTO event_table_general_condensed (repo_name, stars, event_time, repo_created) VALUES (%s, %s, %s, %s)" % (event[0], event[1], event[2], event[3]))
	db.commit()

print "complete"