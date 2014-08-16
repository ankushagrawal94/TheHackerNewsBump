#getExpectedDateOfMention.py

import MySQLdb
import time
import re
import datetime
import json
import requests
from collections import Counter

db = MySQLdb.connect(host="localhost", # your host, usually localhost
	                     user="root", # your username
	                      passwd="password", # your password
	                      db="githubDB") # name of the data base

cur = db.cursor()
cur.execute("DROP TABLE IF EXISTS days_after")
cur.execute("""
	CREATE TABLE days_after( 
		stars 			INT(6),
		hn_points 		INT(6),
		avg_days_after 	INT(6),
		mode_days_after INT(6),
		num_data_points	INT(6))""")
db.commit()


cur.execute("SELECT repo_name, event_time FROM hn_event_max")
hn_event_list = cur.fetchall()

#Globals
github_api_request_counter = 0
event_num = 0
hn_point_params = [5,10,50,100,150,200,250,300,400,500]
gh_point_params = [5,10,50,100,500,1000,2500,5000,7500,10000,20000,30000,40000,50000,60000,70000]
hn_val_counter = 0
start = 0
stop = 160
start_time = time.time()
try:	
	for point_val in hn_point_params:
		gh_point_counter = 0
		hn_val_counter += 1
		for star_val in gh_point_params:
			event_num += 1
			gh_point_counter += 1
			if event_num < start:
				continue
			if event_num > stop:
				continue
			try:
				cur.execute("SELECT * FROM hn_event_max WHERE stars BETWEEN %s AND %s AND hn_points BETWEEN %s AND %s" % (star_val, gh_point_params[gh_point_counter], point_val, hn_point_params[hn_val_counter]))
			except:
				try:
					cur.execute("SELECT * FROM hn_event_max WHERE stars > %s AND hn_points BETWEEN %s AND %s" % (star_val, point_val, hn_point_params[hn_val_counter]))
				except:
					cur.execute("SELECT * FROM hn_event_max WHERE stars > %s AND hn_points > %s" % (star_val, point_val))
			hn_event_list = cur.fetchall()

			if len(hn_event_list) == 0:
				print "Skipping event# %s; No big_pic with %s points and %s stars" % (event_num, star_val, point_val)
				continue

			num_days_avg = 0
			num_days_after = []

			for hn_event in hn_event_list:
				hn_repo_name = hn_event[0]
				hn_event_time = hn_event[3]
				if hn_repo_name[0] == '/':
					print "skipping"
					continue

				repo_url = 'https://api.github.com/repos/%s' % hn_repo_name
				#print "beginngin API call"
				repo_reponse = requests.get(repo_url, auth = ('lvt001@ucsd.edu', 'Vietlong812'))
				#print "completed API call"
				github_api_request_counter += 1
				repo_decoded = json.loads(repo_reponse.text)

				try:
					created_at = repo_decoded["created_at"]
					created_at = created_at[:10]
					#print "created at is %s" % created_at
				except:
					print "No created at field"
					continue

				try:
					date_object = datetime.datetime.strptime(created_at, '%Y-%m-%d')
					diff = hn_event_time - date_object.date()
					num_diff = diff.microseconds + (diff.seconds + diff.days * 86400)
					if diff.total_seconds() < 0:
						continue
					num_days_after.append(diff.total_seconds()/3600/24)
					#print num_days_after
				except Exception, e:
					print e
					print "Could not subtract times"
					continue

			print "\nnum days after array shows: %s" % num_days_after

			for num in num_days_after:
				num_days_avg += num

			try:
				num_days_avg /= len(num_days_after)
			except Exception, e:
				print "No data points acquired"
				print e
				continue
			print "average number of days is: %s" % num_days_avg

			data = Counter(num_days_after)
			mode = data.most_common(1)
			modeVal = mode[0][0]
			print "most common number of days after is: %s" % modeVal

			num_data_points = len(num_days_after)

			print "inserting data"
			cur.execute("""	INSERT INTO days_after (stars, hn_points, avg_days_after, mode_days_after, num_data_points) 
							VALUES (%s, %s, %s, %s, %s)""", (star_val, point_val, int(num_days_avg), modeVal, num_data_points))		

			db.commit()
			print "elapsed time is: %s seconds" % (int(time.time() - start_time))
			print "completed %s of %s \n \n" % (event_num, 160)
except Exception, e:
	print e
	print "Elapsed time is: %s seconds" % (time.time() - start_time)
	print "Terminating Execution"


			