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

event_num = 0
start = 140
stop = 155

try:
	
	hn_point_params = [5,10,50,100,150,200,250,300,400,500]
	gh_point_params = [5,10,50,100,500,1000,2500,5000,7500,10000,20000,30000,40000,50000,60000,70000]
	for point_val in hn_point_params:
		for star_val in gh_point_params:
			event_num += 1
			if event_num < start:
				continue
			if event_num > stop:
				continue
			print "You are on event #%s of %s" % (event_num, int(len(hn_point_params) * len(gh_point_params)))
			print "Beginning analysis for hn_points = %s & gh_stars = %s" % (point_val, star_val)
			print "Total elapsed time is: %s seconds" % int(time.time() - start_time)
			
			cur.execute("SELECT * FROM hn_event_max WHERE stars > %s AND hn_points > %s" % (star_val, point_val))
			hn_event_list = cur.fetchall()

			if len(hn_event_list) == 0:
				print "Skipping event# %s; No events with %s points and %s stars" % (event_num, star_val, point_val)
				continue
			global_percent_change = [0] * 14
			global_percent_avg = [0] * 14
			global_raw_stars = [0] * 15
			global_raw_star_avg = [0] * 15
			event_count = 0
			prev_row = ''

			for event in hn_event_list:
				#12938 events before duplicates
				#8237 after removing duplicates
				event_count += 1

				repo_name = event[0]
				stars = event[1]
				hn_points = event[2]
				event_time = event[3]

				if event[0] == prev_row:
					prev_row = event[0]
					continue
				else:
					prev_row = event[0]

				raw_num_stars = []
				repo_percent_change = []
				print "Beginning analysis for: %s" % repo_name
				print "total elapsed time is: %s seconds" % int(time.time() - start_time)
				#Get all 15 days
				i = -7
				prev_val = 0
				prev_day_stars = 0
				insuffecient_data = 0
				while i < 8:
					if insuffecient_data > 3:
						i += 1
						continue
					prev_day = event_time + datetime.timedelta(days = i)
					cur.execute(("SELECT stars FROM event_table WHERE event_time = \"%s\" AND repo_name = \"%s\"") % (prev_day, repo_name))
					
					flag = False

					for row in cur.fetchall():
						prev_day_stars = row[0]
						flag = True

					if prev_day_stars == 0:
						insuffecient_data += 1

					if not flag:
						raw_num_stars.append(float(prev_val))
					else:
						raw_num_stars.append(float(prev_day_stars))
					prev_val = prev_day_stars	
					i += 1
				if insuffecient_data > 3:
					print "insuffecient_data"
					continue
				print "total elapsed time is: %s seconds" % int(time.time() - start_time)
				
				print "Fixing Erroneous Data from: "
				print raw_num_stars
				
				i = 0
				raw_star_count = 0
				while i < 15:
					raw_star_count += raw_num_stars[i]
					i += 1
				if raw_star_count == 0:
					print "print all zero data. Skipping"
					continue

				i = 0
				first_non_zero = 0
				while i < 15:
					if raw_num_stars[i] != 0:
						first_non_zero = raw_num_stars[i]
						break
					i += 1

				if raw_num_stars[0] == 0:
					raw_num_stars[0] = first_non_zero

				i = 1
				while i < 15:
					if raw_num_stars[i] == 0:
						raw_num_stars[i] = raw_num_stars[i-1]
					i += 1

				i = 0
				raw_star_count = 0
				while i < 15:
					raw_star_count += raw_num_stars[i]
					i += 1
				if raw_star_count == 0:
					print "RAW STAR COUNT IS 0. SHOULD NOT BE. SKIPPING THIS DATA POINT"
					break

				print "Adjusted Data is: "
				print raw_num_stars
				
				print "processing list"

				#Process the list
				i = 1
				while i < 15:	
					repo_percent_change.append((float(raw_num_stars[i]) - float(raw_num_stars[i - 1]))/float(raw_num_stars[i - 1]))
					i += 1

				i = 0
				while i < len(repo_percent_change):
					global_percent_change[i] += repo_percent_change[i]
					i += 1

				i = 0
				while i < len(raw_num_stars):
					global_raw_stars[i] += raw_num_stars[i]
					i += 1

				print "repo name is: %s" % repo_name 
				print "global raw stars is %s" % global_raw_stars
				print "repo percent change is %s" % repo_percent_change
				print "global percent change is %s" % global_percent_change
				print "completed event #%s of %s" % (event_count, len(hn_event_list))
				print "total elapsed time is: %s seconds" % int(time.time() - start_time)
				print "average time per repo is: %s seconds" % int((time.time() - start_time)/event_count)
				print '\n\n--------------------------------------'

			print "calculating global data..."
			global_percent_change.insert(0,0)
			global_raw_stars.insert(0,0)

			global_percent_avg = (x/len(hn_event_list) for x in global_percent_change)
			global_raw_star_avg = (x/len(hn_event_list) for x in global_raw_stars)

			base = 1
			total_sum = base
			i = 0
			while i < 14:
				total_sum *= (1 + global_percent_change[i])
				i += 1
			mid = base
			i = 0
			while i < 8:
				mid *= (1 + global_percent_change[i])
				i += 1

			global_delta_growth = ((total_sum - mid)/mid - (mid - base)/base)/((mid - base)/base)

			inner_db = MySQLdb.connect(host="localhost", # your host, usually localhost
				                     user="root", # your username
				                      passwd="password", # your password
				                      db="githubDB") # name of the data base

			#write new data to database
			print "Writing to chart_table"
			inner_cur = inner_db.cursor() 

			global_percent_avg.insert(0,0)
			global_raw_star_avg.insert(0,0)
			for event in hn_event_list: #iterate through events
				i = 0
				repo_name = event[0]
				stars = event[1]
				hn_points = event[2]
				while i < 15: #iterates through the days

					inner_cur.execute("""INSERT INTO chart_table (day, slider_stars, slider_hn_points, daily_total_stars, daily_growth, change_in_growth) 
								VALUES (%s, %s, %s, %s, %s, %s)""", (i, stars, hn_points, global_raw_star_avg[i], global_percent_avg[i], global_delta_growth))
					i += 1
					inner_db.commit()

			inner_cur.close()
			inner_db.close()
			print "data insertion complete"

			print "global raw star average is: %s" % (global_raw_star_avg)
			print "global percent average is: %s" % (global_percent_avg)
			print "gloabl delta growth is: %s" % (global_delta_growth)
			print "completed data set #%s of %s" % (event_num, len(hn_point_params) * len(gh_point_params))
			print "total elapsed time is: %s seconds" % int(time.time() - start_time)
			print "average time per overall request is: %s seconds" % int((time.time() - start_time)/event_num)
			print '\n\n\n--------------------------------------'

			cur.close()
			db.close()
except Exception, e:
	print e 
	print 'Keyboard interupt received.'
finally:
	print "start: %s" % start
	print "stop: %s" % stop
	print "event_num: %s" % event_num
	print "total elapsed time: %s" % (time.time() - start_time)
