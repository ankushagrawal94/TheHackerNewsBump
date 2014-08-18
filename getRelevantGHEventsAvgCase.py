#This file gets all the GitHub events from event_table that are relevant where relevance is defined as within 1 week of expected_hn_mention_date

import MySQLdb
import time
import re
import datetime

start_time = time.time()


db = MySQLdb.connect(host="localhost", # your host, usually localhost
	                     user="root", # your username
	                      passwd="password", # your password
	                      db="githubDB") # name of the data base

cur = db.cursor() 
cur.execute ("USE githubDB")
cur.execute("DROP TABLE IF EXISTS event_table_general_condensed")
cur.execute ("""
	CREATE TABLE event_table_general_condensed
	(
		repo_name   	VARCHAR(255),
		stars       	INT(6),
		event_time		DATE, 
		repo_created	DATE
	)
""")
db.commit()
print "succesfully created the DB"

cur.execute("SELECT * FROM days_after")
days_after = cur.fetchall()
#calculate avg_days_after
days_used = 0
avg_days_after = 0
for day in days_after:
	d_stars = day[0]
	d_hn_points = day[1]
	d_avg_days_after = day[2]
	d_mode_days_after = day[3]
	d_num_data_points = day[4]
	if d_num_data_points < 10:
		continue
	avg_days_after += d_avg_days_after
	days_used += 1

avg_days_after /= days_used
print "The average number of days after is: %s" % avg_days_after
#Get a list of all repositories with their respective creation dates and current number of stars
cur.execute("SELECT * FROM latest_repo_events WHERE stars > 5")
global_event_list = cur.fetchall()

prev_row = ''
event_count = 0
#Iterate through this list and look for events in the 7 days before and after the expected_hn_mention_date. 
#Put this in a table called event_table_general_condensed.
for event in global_event_list:
	event_count += 1
	repo_name = event[0]
	stars = event[1]
	event_time = event[2]
	repo_created = event[3]

	#skip duplicates
	if event[0] == prev_row:
		prev_row = event[0]
		continue
	prev_row = event[0]
	#352
	expected_hn_mention_date = repo_created + datetime.timedelta(days = avg_days_after)
	#Get all 15 days
	start_date = expected_hn_mention_date + datetime.timedelta(days = -7)
	end_date = expected_hn_mention_date + datetime.timedelta(days = 7)
	cur.execute(("SELECT * FROM event_table_two WHERE repo_name = \"%s\" AND event_time BETWEEN \"%s\" AND \"%s\" ") % (repo_name, start_date, end_date))
	
	prev_entry = ''
	for row in cur.fetchall():
		#ET refers to event_table
		ET_repo_name = row[0]
		ET_stars = row[1]
		ET_event_time = row[2]
		ET_repo_created = row[3]
		if prev_entry == ET_event_time:
			continue
		prev_entry = ET_repo_created
		cur.execute(("INSERT INTO event_table_general_condensed (repo_name, stars, event_time, repo_created) VALUES (%s, %s, %s, %s)"), (ET_repo_name, ET_stars, ET_event_time, ET_repo_created))
		db.commit()

	print "completed event #%s of %s" % (event_count, len(global_event_list))
	print "time elapsed is: %s seconds" % int(time.time() - start_time)
	try:
		print "Expected time until completion: %s seconds" %  (int((time.time() - start_time) / ( float(event_count)/len(global_event_list) )) - int(time.time() - start_time))
	except Exception, e:
		print e

print "\n\nEvent collection complete."





