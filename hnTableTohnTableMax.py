#This file gets the most relevant HN event for each repo as determined by the number of upvotes recieved

import MySQLdb
import time

conn = MySQLdb.connect(host = "localhost", user = "root", passwd = "password")
cursor = conn.cursor()
#cursor.execute ("DROP DATABASE IF EXISTS githubDB")
##cursor.execute ("CREATE DATABASE githubDB")
cursor.execute ("USE githubDB")
cursor.execute("DROP TABLE IF EXISTS hn_event_max")
cursor.execute ("""
	CREATE TABLE hn_event_max
	(
		repo_name   VARCHAR(255),
		stars       INT(6),
		hn_points	INT(6),
		event_time  DATE
	)
	""")
conn.commit()
print "succesfully created hn_event_max"

cursor.close()
conn.close()

try:
	print "started"
	startTime = time.time()

	db = MySQLdb.connect(host="localhost", # your host, usually localhost
	                     user="root", # your username
	                      passwd="password", # your password
	                      db="githubDB") # name of the data base

	cur = db.cursor() 
	cur.execute(""" INSERT INTO hn_event_max
    SELECT y.repo_name, y.stars, y.hn_points, y.event_time
	FROM hn_event_table_two y 
	INNER JOIN (SELECT repo_name, max(hn_points) as max_points
			FROM hn_event_table_two x
			GROUP BY repo_name) x
	ON y.repo_name = x.repo_name
	AND x.max_points = y.hn_points
	ORDER BY repo_name ASC""")
	db.commit()

	stopTime = time.time()
	elapsedTime = stopTime - startTime
	print elapsedTime
	# print all the first cell of all the rows
	for row in cur.fetchall() :
	    print str(row[0]) + '\t\t\t\t' + str(row[1])

	cur.close()
	db.close()
except Exception, e:
	print e
	raise e


