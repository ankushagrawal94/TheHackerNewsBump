import MySQLdb
import time

startTime = time.time()

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="password", # your password
                      db="masterDB") # name of the data base

cur = db.cursor() 

cur.execute("""SELECT y.repo_name, y.stars 
	FROM event_table y 
	INNER JOIN (SELECT repo_name, max(event_time) as recent
			FROM event_table x
			GROUP BY repo_name) x
	ON y.repo_name = x.repo_name
	AND x.recent = y.event_time""")

# print all the first cell of all the rows
for row in cur.fetchall() :
    print str(row[0]) + '\t\t\t\t' + str(row[1])

cur.close()
db.close()

stopTime = time.time()
elapsedTime = stopTime - startTime
