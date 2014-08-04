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

strHH = str(3)
strDD = str(11)
strMM = str(3)
strYY = str(12)
if len(strDD) == 1:
    strDD = "0" + strDD
if len(strMM) == 1:
    strMM = "0" + strMM
print "20" + strYY + "-" + strMM + "-" + strDD + "-" + strHH
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
        	print repo_name + str(num_stars) + created_at
        except Exception, e:
        	print e
        	print "error parsing JSON or error inserting to DB"