import json
from json import JSONDecoder
import re

#decode = json.loads('/Development/GitHubChallenge/2014-03-11-12.json')
#print decode

#shameless copy paste from json/decoder.py
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
#startAt = 1008 #FEB 12 2011
startAt = 10654 #MAR 10
stopAt = 20000
counter = 0
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
                #print strYY + "-" + strMM + "-" + strDD + "-" + strHH
                #f = open ("/Volumes/WD_1TB/GitHub Archive/20"+strYY+"-"+strMM+"-"+strDD+"-"+strHH+".json", 'r')
                try:
                    f = json.load (open ("/Development/GitHubChallenge/JSONData/20"+strYY+"-"+strMM+"-"+strDD+"-"+strHH+".json", 'r') , cls=ConcatJSONDecoder)
                    for each_event in f:
                        if(each_event["type"] == "WatchEvent"):
                            try:
                                num_stars = int(each_event["repository"]["watchers"])
                                created_at = each_event["created_at"]
                            except Exception, e:
                                print e
                except Exception, e:
                    print e


                try:
                                    f = json.load (open ("/Development/GitHubChallenge/JSONData/20"+strYY+"-"+strMM+"-"+strDD+"-"+strHH+".json", 'r'), cls = ConcatJSONDecoder)
                                    for each_event in f:
                                        if(each_event["type"] == "WatchEvent"):
                                            try:
                                                num_stars = int(each_event["repository"]["watchers"])
                                                created_at = each_event["created_at"][:10]
                                                json_entry[4][created_at] = num_stars
                                            except Exception, e:
                                                print e
                                    print json_entry[4]
                                except Exception, e:
                                    print e
                

