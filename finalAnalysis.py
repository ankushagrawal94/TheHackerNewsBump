import MySQLdb
import time
import re
import datetime

db = MySQLdb.connect(host="localhost", # your host, usually localhost
	                     user="root", # your username
	                      passwd="password", # your password
	                      db="githubDB") # name of the data base

cur = db.cursor() 

cur.execute("select * from chart_table_avg")

all_data = cur.fetchall()

count = 0
avg_percent = 0
for dataPoint in all_data:
	count += 1
	avg_percent += dataPoint[5]
avg_percent /= count
print avg_percent

cur.execute("select * from chart_table")

all_data = cur.fetchall()

count = 0
data_percent = 0
for dataPoint in all_data:
	count += 1
	data_percent += dataPoint[5]
data_percent /= count
print data_percent


print "complete"