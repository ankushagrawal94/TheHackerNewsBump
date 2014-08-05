import MySQLdb
import time
import requests
import json
from json import JSONDecoder
import re

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

hn_search_url = 'https://hn.algolia.io/api/v1/search_by_date?query=\"https://github.com/' + 'mojombo/grit' + '\"&tags=story&page=' + str(0)
print hn_search_url
hn_response = requests.get(hn_search_url)
hn_decoded = json.loads(hn_response.text)

for each_hit in hn_decoded["hits"]:
	print "hit"
	theDate = each_hit["created_at"][:10]
	points = each_hit["points"]
	print points
	#YYYY:MM:DD
	#cur.execute ("""INSERT INTO hn_event_table (repo_name, stars, hn_points, event_time) VALUES (%s, %s, %s, %s)""", ('mojombo/grit', '200', theDate)) 
	#db.commit()

for row in cur.fetchall() :
    print str(row[0]) + '\t\t\t\t' + str(row[1]) + '\t\t' + str(row[2])

cur.close()
db.close()
