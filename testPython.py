import MySQLdb
import time

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="password", # your password
                      db="githubDB") # name of the data base

cur = db.cursor() 

startTime = time.time()
cur.execute("SELECT repo_name, stars, event_time FROM max_stars WHERE repo_name = \"mojombo/grit\" ")

count = 0;

for row in cur.fetchall() :
    if row[0] == "mojombo/grit":
        count += 1
print count
stopTime = time.time()
elapsedTime = stopTime - startTime
print elapsedTime

cur.close()
db.close()