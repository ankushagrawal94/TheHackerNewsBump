import MySQLdb
import time
import re
import datetime

start_time = time.time()
elapsed_time = time.time()

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                       user="root", # your username
                        db="dumpDB") # name of the data base

cur = db.cursor() 
cur.execute("SELECT * FROM chart_table")
chart_table = cur.fetchall()

count = 1
for each_row in chart_table:
	print "%s\t%s\t%s\t%s\t%s\t%s" % (each_row[0], each_row[1], each_row[2], each_row[3], each_row[4], each_row[5])
  	if count == 15:
  		count = 0
  		print "\t%s\t%s" % (each_row[1], each_row[2])
  	count += 1
