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
completed_events = 0
big_event_count = 0
start = 0
stop = 160
infinite_growth = 0

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
			print "You are on big_pic #%s of %s" % (event_num, int(len(hn_point_params) * len(gh_point_params)))
			print "Beginning analysis for hn_points = %s & gh_stars = %s" % (point_val, star_val)
			print "Total elapsed time is: %s seconds" % int(time.time() - start_time)
			print "Performing Query ... \n"
			
			cur.execute("SELECT * FROM hn_event_max WHERE stars > %s AND hn_points > %s" % (star_val, point_val))
			hn_event_list = cur.fetchall()

			if len(hn_event_list) == 0:
				print "Skipping event# %s; No big_pic with %s points and %s stars" % (event_num, star_val, point_val)
				continue
			global_percent_change = [0] * 14
			global_percent_avg = [0] * 14
			global_raw_stars = [0] * 15
			global_raw_star_avg = [0] * 15
			event_count = 0
			prev_row = ''
			hn_event_list_size = len(hn_event_list)
			for event in hn_event_list:
				event_count += 1

				repo_name = event[0]
				stars = event[1]
				hn_points = event[2]
				event_time = event[3]

				#skip duplicates
				if event[0] == prev_row:
					prev_row = event[0]
					hn_event_list_size -= 1
					continue
				else:
					prev_row = event[0]

				raw_num_stars = [0] * 15
				repo_percent_change = []
				print "Beginning analysis for: %s" % repo_name
				#print "total elapsed time is: %s seconds" % int(time.time() - start_time)
				#Get all 15 days
				
				daily_event_times = [] 		#store event times for each day
				daily_star_count = []		#store stars for each day
				start_date = event_time + datetime.timedelta(days = -7)
				end_date = event_time + datetime.timedelta(days = 7)
				cur.execute(("SELECT * FROM event_table_condensed WHERE repo_name = \"%s\" AND event_time BETWEEN \"%s\" AND \"%s\" ") % (repo_name, start_date, end_date))
				
				flag = False		#tells whether you entered cur.fetchall for loop
				for row in cur.fetchall():
					#ET refers to event_table
					ET_repo_name = row[0]
					ET_stars = row[1]
					ET_event_time = row[2]
					#cur.execute(("INSERT INTO event_table_condensed (repo_name, stars, event_time) VALUES (%s, %s, %s)"), (ET_repo_name, ET_stars, ET_event_time))
					#db.commit()
					daily_event_times.append(ET_event_time)
					daily_star_count.append(ET_stars)
					flag = True

				i = 0
				while i < 15:
					curr_day = start_date + datetime.timedelta(days = i)
					try:
						indexOfDay = daily_event_times.index(curr_day)
						raw_num_stars[indexOfDay] = daily_star_count[indexOfDay]
					except Exception, e:
						pass
					i += 1

				print "total elapsed time is: %s seconds" % int(time.time() - start_time)
				
				#print "Fixing Erroneous Data from: "
				#print raw_num_stars
				
				i = 0
				raw_star_count = 0
				while i < 15:
					raw_star_count += raw_num_stars[i]
					i += 1
				if raw_star_count == 0:
					hn_event_list_size -= 1
					print "All zero data. Skipping"
					print '--------------------------------------'
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
				while i < len(raw_num_stars):
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

				#print "Adjusted Data is: "
				#print raw_num_stars
				
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
				completed_events += 1
				#print "the raw_num_stars is:"
				#print raw_num_stars

				#print "the global_raw_stars is:"
				#print global_raw_stars

				#print "repo name is: %s" % repo_name 
				#print "global raw stars is %s" % global_raw_stars
				#print "repo percent change is %s" % repo_percent_change
				#print "global percent change is %s" % global_percent_change
				print "\ncompleted event #%s of %s" % (event_count, hn_event_list_size)
				print "total elapsed time is: %s seconds" % int(time.time() - start_time)
				print "average time per repo is: %s seconds" % int((time.time() - start_time)/completed_events)
				print '--------------------------------------'

			i = 0
			raw_star_count = 0
			while i < 15:
				raw_star_count += global_raw_stars[i]
				i += 1
			if raw_star_count == 0:
				print "All zero data. Skipping"
				print '--------------------------------------'
				continue

			print "calculating global data..."
			global_percent_change.insert(0,0)
			global_percent_avg.insert(0,0)

			i = 0
			while i < len(global_percent_change):
				global_percent_avg[i] = global_percent_change[i]/hn_event_list_size
				global_raw_star_avg[i] = global_raw_stars[i]/hn_event_list_size
				i += 1
			i = 0
			while i < len(global_raw_stars):
				global_raw_star_avg[i] = global_raw_stars[i]/hn_event_list_size
				i += 1
			print "successfully created global_percent_avg and global_raw_star_avg"
			
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

			print total_sum
			print mid
			print base
			print global_percent_change
			print global_raw_star_avg
			print global_raw_stars
			print hn_event_list_size

			try:
				global_delta_growth = ((total_sum - mid)/mid - (mid - base)/base)/((mid - base)/base)
				print "successfully created global_delta_growth to be: %s" % global_delta_growth
			except:
				infinite_growth += 1
				print "infinite growth"
				continue

			inner_db = MySQLdb.connect(host="localhost", # your host, usually localhost
				                     user="root", # your username
				                      passwd="password", # your password
				                      db="githubDB") # name of the data base

			#write new data to database
			print "Writing to chart_table_three ...\n"
			inner_cur = inner_db.cursor() 

			i = 0
			while i < 15: #iterates through the days
				inner_cur.execute("""INSERT INTO chart_table_three (day, slider_stars, slider_hn_points, daily_total_stars, daily_growth, change_in_growth) 
							VALUES (%s, %s, %s, %s, %s, %s)""", (i, star_val, point_val, global_raw_star_avg[i], global_percent_avg[i]*100, global_delta_growth))
				i += 1
				inner_db.commit()

			inner_cur.close()
			inner_db.close()
			big_event_count += 1
			print '\n\n\n--------------------------------------'
			print "data insertion complete\n"
			print "Summary for %s hn_points and %s stars." % (point_val, star_val)
			print "global raw star average is: %s" % (global_raw_star_avg)
			print "global percent average is: %s" % (global_percent_avg)
			print "global delta growth is: %s" % (global_delta_growth)
			print "completed data set #%s of %s" % (event_num, len(hn_point_params) * len(gh_point_params))
			print "total elapsed time is: %s seconds" % int(time.time() - start_time)
			print "average time per overall request is: %s seconds" % int((time.time() - start_time)/completed_events)
			print "expected time remaining is: %s" % (int((time.time() - start_time)/completed_events) * int(len(hn_point_params) * len(gh_point_params)))
			print '\n\n\n--------------------------------------'

except Exception, e:
	print e 
	print 'Keyboard interupt received.'
finally:
	print '\n--------------------------------------'
	print '--------------------------------------'
	print "start: %s" % start
	print "stop: %s" % stop
	print "big event completed #%s" % big_event_count
	print "event_num: %s" % event_num
	print "infinite_growth occured %s times" % infinite_growth
	print "total elapsed time: %s" % (time.time() - start_time)
	print '\n--------------------------------------'
	cur.close()
	db.close()
