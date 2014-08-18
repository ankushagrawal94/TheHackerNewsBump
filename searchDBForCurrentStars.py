#searchDBForCurrentStars.py is reponsible for getting the most recent entry for each repository

import MySQLdb
import time

conn = MySQLdb.connect(host = "localhost", user = "root", passwd = "password")
cursor = conn.cursor()
#cursor.execute ("DROP DATABASE IF EXISTS githubDB")
##cursor.execute ("CREATE DATABASE githubDB")
cursor.execute ("USE githubDB")
cursor.execute("DROP TABLE IF EXISTS latest_repo_events")
cursor.execute ("""
	CREATE TABLE latest_repo_events
	(
		repo_name   	VARCHAR(255),
		stars       	INT(6),
		event_time		DATE, 
		repo_created	DATE
	)
""")
conn.commit()
print "succesfully created the DB"

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
	cur.execute(""" INSERT INTO latest_repo_events
    SELECT y.repo_name, y.stars, y.event_time, y.repo_created
	FROM event_table_two y 
	INNER JOIN (SELECT repo_name, max(event_time) as recent
			FROM event_table_two x
			GROUP BY repo_name) x
	ON y.repo_name = x.repo_name
	AND x.recent = y.event_time""")
	db.commit()

	stopTime = time.time()
	elapsedTime = stopTime - startTime
	print elapsedTime

	cur.close()
	db.close()
except Exception, e:
	print e
	raise e


