#This file gets all the GitHub events from event_table that are relevant where relevance is defined as within 1 week of being mentioned on HN

import MySQLdb
import time
import re
import datetime

db = MySQLdb.connect(host="localhost", # your host, usually localhost
	                     user="root", # your username
	                      passwd="password", # your password
	                      db="githubDB") # name of the data base

cur = db.cursor() 

cur.execute("SELECT * FROM hn_event_max WHERE stars > 5 AND hn_points > 5")
hn_event_list = cur.fetchall()

prev_row = ''
for event in hn_event_list:
	repo_name = event[0]
	stars = event[1]
	hn_points = event[2]
	event_time = event[3]

	#skip duplicates
	if event[0] == prev_row:
		prev_row = event[0]
		continue
	else:
		prev_row = event[0]

	#Get all 15 days
	start_date = event_time + datetime.timedelta(days = -7)
	end_date = event_time + datetime.timedelta(days = 7)
	cur.execute(("SELECT * FROM event_table WHERE repo_name = \"%s\" AND event_time BETWEEN \"%s\" AND \"%s\" ") % (repo_name, start_date, end_date))
	
	for row in cur.fetchall():
		#ET refers to event_table
		ET_repo_name = row[0]
		ET_stars = row[1]
		ET_event_time = row[2]
		cur.execute(("INSERT INTO event_table_condensed (repo_name, stars, event_time) VALUES (%s, %s, %s)"), (ET_repo_name, ET_stars, ET_event_time))
		db.commit()
