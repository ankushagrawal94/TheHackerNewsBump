import MySQLdb
import time
import re
import datetime

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      db="dumpDB") # name of the data base

cur = db.cursor() 

cur.execute("SELECT * FROM hn_event_table WHERE stars > 1000 AND hn_points > 10 LIMIT 4")
hn_event_list = cur.fetchall()

global_percent_change = [0] * 14
global_percent_avg = [0] * 14

for event in hn_event_list:
	repo_name = event[0]
	stars = event[1]
	hn_points = event[2]
	event_time = event[3]

	raw_num_stars = []
	repo_percent_change = []

	print repo_name

	#Get all 15 days
	i = -7
	prev_val = 0
	prev_day_stars = 0
	while i < 8:
		print 'Day: %s' % i
		prev_day = event_time + datetime.timedelta(days = i)
		cur.execute(("SELECT stars FROM event_table WHERE event_time = \"%s\" AND repo_name = \"%s\"") % (prev_day, repo_name))
		
		flag = False

		for row in cur.fetchall():
			prev_day_stars = row[0]
			flag = True

		print 'prev_val: %s' % prev_val
		print 'stars this day: %s' % prev_day_stars
		
		if not flag:
			raw_num_stars.append(float(prev_val))
		else:
			raw_num_stars.append(float(prev_day_stars))
		prev_val = prev_day_stars	

		i += 1
		print raw_num_stars
	print '\n\n--------------------------------------'

	print raw_num_stars
	print '\n\n'

	

	#Process the list
	i = 1
	while i < 15:	
		repo_percent_change.append((float(raw_num_stars[i]) - float(raw_num_stars[i - 1]))/float(raw_num_stars[i - 1]))
		i += 1

	i = 0
	while i < len(repo_percent_change):
		global_percent_change[i] += repo_percent_change[i]
		i += 1

	print repo_percent_change
	print global_percent_change
global_percent_avg = (x/len(hn_event_list) for x in global_percent_change)


base = 1
total_sum = base
while total_sum < 15:
	total_sum *= (1 + global_percent_change[i])
mid = base
while mid < 8:
	mid *= (1 + global_percent_change[i])

global_delta_growth = ((total_sum - mid)/mid - (mid - base)/base)/((mid - base)/base)


print global_percent_avg
print '\n'

cur.close()
db.close()