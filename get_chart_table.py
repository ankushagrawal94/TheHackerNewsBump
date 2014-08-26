import MySQLdb
import time
import re
import datetime

start_time = time.time()
elapsed_time = time.time()

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                       user="root", # your username
                        db="githubDB") # name of the data base

f = open('chart_table.txt', 'w')
f2 = open('chart_table_avg.txt', 'w')

cur = db.cursor() 
cur.execute("SELECT * FROM chart_table")
chart_table_gen = cur.fetchall()

stars_array = [5, 10, 50, 100, 500, 1000, 2500, 5000, 7500, 10000, 20000, 30000, 40000, 50000, 60000, 70000];
hn_array = [5, 10, 50, 100, 150, 200, 250, 300, 400, 500];

content = ''
row_index = 0

chart_table = []
for each_row in chart_table_gen:
	chart_table.append(each_row)

tmp_i = []
tmp_y = []

tuples_list = []
orgin_tuple_list = []

for each in chart_table:
	orgin_tuple_list.append((each[1], each[2]))

for i in stars_array:
	for y in hn_array:
		print "star array %s \t chart_table %s \t hn_array %s chart_table %s" % (i, chart_table[row_index][1], y, chart_table[row_index][2])
		
		for each in chart_table:
			com_tup = (i, y)
			if i == each[1] and y == each[2]:
				print 'if %s %s ' % (i, y)
				content += "%s\t%s\t%s\t%s\t%s\t%s\t0\n" % (each[0], each[1], each[2], each[3], each[4], each[5])
				continue
			else:
				print "enter else \t i %s each[i] %s y %s each[2] %s" % (i, each[1], y, each[2])
				if com_tup not in tuples_list and com_tup not in orgin_tuple_list:
					print tuples_list
					tup = (i, y)
					tuples_list.append(tup)

for each in tuples_list:
	for tmp_count in range(16):
		print '%s \t %s ' % (each[0], each[1])
		content += "%s\t%s\t%s\t%s\t%s\t%s\t0\n" % (tmp_count, each[0], each[1], 0, 0, 0)

f.write(content)



content = ''
cur.execute("SELECT * FROM chart_table_avg")
chart_table_gen = cur.fetchall()
chart_table = []
for each_row in chart_table_gen:
	chart_table.append(each_row)

tmp_i = []
tmp_y = []

tuples_list = []
orgin_tuple_list = []

for each in chart_table:
	orgin_tuple_list.append((each[1], each[2]))

for i in stars_array:
	for y in hn_array:
		print "star array %s \t chart_table %s \t hn_array %s chart_table %s" % (i, chart_table[row_index][1], y, chart_table[row_index][2])
		
		for each in chart_table:
			com_tup = (i, y)
			if i == each[1] and y == each[2]:
				print 'if %s %s ' % (i, y)
				content += "%s\t%s\t%s\t%s\t%s\t%s\t1\n" % (each[0], each[1], each[2], each[3], each[4], each[5])
				continue
			else:
				print "enter else \t i %s each[i] %s y %s each[2] %s" % (i, each[1], y, each[2])
				if com_tup not in tuples_list and com_tup not in orgin_tuple_list:
					print tuples_list
					tup = (i, y)
					tuples_list.append(tup)

for each in tuples_list:
	for tmp_count in range(16):
		print '%s \t %s ' % (each[0], each[1])
		content += "%s\t%s\t%s\t%s\t%s\t%s\t1\n" % (tmp_count, each[0], each[1], 0, 0, 0)

f2.write(content)  	