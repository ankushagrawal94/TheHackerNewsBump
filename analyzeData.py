import requests
import json
from json import JSONDecoder
import re
import MySQLdb

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


since = 0

star_threshold = 1000

github_api_request_counter = 0
algolia_api_request_counter = 0

#startAt = 1008 #FEB 12 2011
startAt = 0 #MAR 10 2012
stopAt = 100000000000
counter = 0

#open mysql DB for use
db = MySQLdb.connect(host="localhost",
                     user="root",
                      passwd="password",
                      db="masterDB")
cur = db.cursor()

#step 1 - Get Links to All Repos
cur.execute("SELECT DISTINCT FROM max_stars")

oldRow = ""
# print all the first cell of all the rows
for row in cur.fetchall():
    #print str(row[0]) + '\t\t\t\t' + str(row[1])
	counter = counter + 1
	if counter < startAt:
		break
	if counter > stopAt:
	 	break
	if str(row[0]) == oldRow:
		print "oldRow is: " + oldRow + "\t newrow is: " + row[0]
		oldRow = str(row[0])
		#print "reached"
		#print oldRow
		continue
	oldRow = str(row[0])
	if row[1] > 1000:
		print str(row[0]) + '\t\t\t\t' + str(row[1])
		hn_incrementor = -1

		while True:
			hn_incrementor += 1
			hn_search_url = 'https://hn.algolia.io/api/v1/search_by_date?query=\"https://github.com/' + row[0] + '\"&tags=story&page=' + str(hn_incrementor)
			hn_response = requests.get(hn_search_url)
			algolia_api_request_counter += 1
			#retrieved the HN search results for a particular repo
			hn_decoded = json.loads(hn_response.text)
			if len(hn_decoded["hits"]) == 0:
				break
			for each_hit in hn_decoded["hits"]:
				#print "HN hit Encountered"
				theDate = each_hit["created_at"][:10]
				points = each_hit["points"]
				#step 5 - store data to MySQL DB
				cur.execute ("""INSERT INTO hn_event_table (repo_name, stars, hn_points, event_time) VALUES (%s, %s, %s, %s)""", (row[0], row[1], points, theDate)) 
				db.commit()			
print algolia_api_request_counter
print counter






























