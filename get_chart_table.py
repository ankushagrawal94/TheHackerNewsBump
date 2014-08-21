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
chart_table = cur.fetchall()

content = ''
for each_row in chart_table:
	content += "%s\t%s\t%s\t%s\t%s\t%s\t0\n" % (each_row[0], each_row[1], each_row[2], each_row[3], each_row[4], each_row[5])
  	

f.write(content)

content = ''
cur.execute("SELECT * FROM chart_table_avg")
chart_table = cur.fetchall()

for each_row in chart_table:
	content += "%s\t%s\t%s\t%s\t%s\t%s\t1\n" % (each_row[0], each_row[1], each_row[2], each_row[3], each_row[4], each_row[5])
  	

f2.write(content)