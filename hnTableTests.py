import MySQLdb
import time
import requests
import json
from json import JSONDecoder
import re

start_time = time.time()
conn = MySQLdb.connect(host = "localhost", user = "root", passwd = "password")
cursor = conn.cursor()
#cursor.execute ("DROP DATABASE IF EXISTS masterDB")
#cursor.execute ("CREATE DATABASE masterDB")
cursor.execute ("USE masterDB")
cursor.execute("DROP TABLE IF EXISTS hn_event_table")
cursor.execute ("""
	CREATE TABLE hn_event_table
	(
		repo_name   VARCHAR(255),
		stars       INT(6),
		hn_points	INT(6),
		event_time  DATE
	)
""")
conn.commit()
print "succesfully created the DB"

cursor.close()
conn.close()

db = MySQLdb.connect(host="localhost", # your host, usually localhost
	                     user="root", # your username
	                      passwd="password", # your password
	                      db="masterDB") # name of the data base

cur = db.cursor() 

cur.execute("SELECT * FROM max_stars WHERE stars > 10")

hn_incrementor = -1

prev_row = ''

api_counter = 0
row_counter = 0
start = 0000
stop = 100000

try:
	for row in cur.fetchall():
		row_counter += 1
		print row_counter
		if row_counter < start:
			continue
		if row_counter > stop:
			continue
		print row

		if row[0] == prev_row:
			prev_row = row[0]
			continue
		else:
			prev_row = row[0]

		#print row

		hn_incrementor = 0
		while True:
			try:
				hn_incrementor += 1
				hn_search_url = 'https://hn.algolia.io/api/v1/search_by_date?query=\"https://github.com/' + row[0] + '\"&tags=story&page=' + str(hn_incrementor)
				print hn_search_url
				hn_response = requests.get(hn_search_url)
				hn_decoded = json.loads(hn_response.text)
				api_counter += 1
				
				if len(hn_decoded["hits"]) == 0:
					break

				for each_hit in hn_decoded["hits"]:
					print "\n\nhit"
					theDate = each_hit["created_at"][:10]
					thePoint = each_hit["points"]
					#YYYY:MM:DD
					cur.execute ("""INSERT INTO hn_event_table (repo_name, stars, hn_points, event_time) VALUES (%s, %s, %s, %s)""", (row[0], row[1], thePoint, theDate)) 
					db.commit()
			except Exception, e:
				print 'Exception hit!'
				print e
				print 'Sleeping for 10s.'
				time.sleep(10)
				hn_incrementor -= 1
except Exception, e:
	print 'Outside exception.'
	print e
	raise e

except: 
	print 'Keyboard interupt received.'
finally:
	print 'start: %s' % start
	print 'stop: %s' % stop
	print 'api_counter: %s' % api_counter
	print 'row_counter: %s' % row_counter
	print time.time() - start_time
 
for row in cur.fetchall() :
    print str(row[0]) + '\t\t\t\t' + str(row[1]) + '\t\t' + str(row[2])

cur.close()
db.close()
