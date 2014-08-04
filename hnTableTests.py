import MySQLdb
import time

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

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor() 

hn_search_url = 'https://hn.algolia.io/api/v1/search_by_date?query=\"https://github.com/' + 'mojombo/grit' + '\"&tags=story&page=' + str(hn_incrementor)
hn_response = requests.get(hn_search_url)
hn_decoded = json.loads(hn_response.text)

if len(hn_decoded["hits"]) == 0:
	break

for each_hit in hn_decoded["hits"]:
	theDate = each_hit["created_at"][:10]
	#YYYY:MM:DD
	theSQLDate = theDate[:3] + '-' + theDate[5:6] + '-' + theDate [8-9]
	print "beginning step 5"
	cur.execute ("""INSERT INTO hn_event_table (repo_name, stars, event_time) VALUES (%s, %s, %s)""", ('mojombo/grit', '200', theSQLDate)) 
	db.commit()


# print all the first cell of all the rows
for row in cur.fetchall() :
    print str(row[0]) + '\t\t\t\t' + str(row[1]) + '\t\t' + str(row[2])

cur.close()
db.close()

cursor.execute ("""INSERT INTO event_table (repo_name, stars, event_time) VALUES (%s, %s, %s)""", (repo_name, str(num_stars), created_at)) 
