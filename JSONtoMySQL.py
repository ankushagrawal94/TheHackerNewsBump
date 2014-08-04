import MySQLdb
import json
from json import JSONDecoder
import re

FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL
WHITESPACE = re.compile(r'[ \t\n\r]*', FLAGS)

class ConcatJSONDecoder(json.JSONDecoder):
    def decode(self, s, _w=WHITESPACE.match):
        s_len = len(s)

        objs = []
        end = 0
        while end != s_len:
            obj, end = self.raw_decode(s, idx=_w(s, end).end())
            end = _w(s, end).end()
            objs.append(obj)
        return objs

#decoded = json.load(open('2014-03-11-12.json'), cls=ConcatJSONDecoder)
#for each_event in decoded:
#	if(each_event["type"] == "WatchEvent"):
#		print each_event["repository"]["watchers"]



conn = MySQLdb.connect(host = "localhost", user = "root", passwd = "password")
cursor = conn.cursor()
#cursor.execute ("DROP DATABASE IF EXISTS masterDB")
#cursor.execute ("CREATE DATABASE masterDB")
#cursor.execute ("USE masterDB")
#cursor.execute ("""
#	CREATE TABLE event_table
#	(
#		repo_name   VARCHAR(255),
#		stars       INT(6),
#		event_time  DATE
#		)
#""")
#conn.commit()
#print "succesfully reset the DB"

#startAt = 1008 #FEB 12 2011
startAt = 10654 #MAR 10 2012. They didn't record the number of stars prior to this date
#startAt = 20000
stopAt = 100000
counter = 0
good = 0
processedFiles = 0
try:
	for yy in range(11,15):
	    for mm in range(1,13):
	        for dd in range(1,32):
	            for hh in range(0,24):
	                counter = counter + 1
	                if counter < startAt:
	                    continue    
	                if counter > stopAt:
	                    continue
	                #print counter
	                strHH = str(hh)
	                strDD = str(dd)
	                strMM = str(mm)
	                strYY = str(yy)
	                if len(strDD) == 1:
	                    strDD = "0" + strDD
	                if len(strMM) == 1:
	                    strMM = "0" + strMM
	                    processedFiles += 1
	                print "20" + strYY + "-" + strMM + "-" + strDD + "-" + strHH + "\t\t" + "count is: " + str(counter) + "\t\tsuccesful entries is: " + str(good) + "\tProcessed Files is: " + str(processedFiles)
	                try:
	                    f = json.load (open ("/Volumes/WD_1TB/GitHub Archive/20"+strYY+"-"+strMM+"-"+strDD+"-"+strHH+".json", 'r') , cls=ConcatJSONDecoder)
	                    for each_event in f:
	                        if(each_event["type"] == "WatchEvent"):
	                            try:
	                            	try:
	                            		repo_name = each_event["repository"]["full_name"]
	                            	except Exception, e:
	                            		repo_name = each_event["repository"]["owner"] + "/" + each_event["repository"]["name"]
	                                num_stars = int(each_event["repository"]["watchers"])
	                                created_at = '20'+strYY+'-'+strMM+'-'+strDD
	                                cursor.execute ("""INSERT INTO event_table (repo_name, stars, event_time)
										VALUES (%s, %s, %s)""", (repo_name, str(num_stars), created_at))
	                                conn.commit()
	                                good = good + 1
	                            except Exception, e:
	                                print e
	                                print "error parsing JSON or error inserting to DB for file: " + "20" + strYY + "-" + strMM + "-" + strDD + "-" + strHH
	                except Exception, e:
	                    print e
	                    print "error reading file: " + "20" + strYY + "-" + strMM + "-" + strDD + "-" + strHH
except Exception, e:
	raise e
except:
	print "keyboard interrupt recieved"
	print "summary: "
	print "You started At: " + str(startAt)
	print "You stopped At: " + str(stopAt)
	print "Counter reached: " + str(counter)

cursor.close()
conn.close()




db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="password", # your password
                      db="masterDB") # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor() 

# Use all the SQL you like
cur.execute("SELECT * FROM event_table")

# print all the first cell of all the rows
for row in cur.fetchall() :
    print str(row[0]) + '\t\t\t\t' + str(row[1]) + '\t\t' + str(row[2])