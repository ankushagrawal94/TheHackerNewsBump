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


