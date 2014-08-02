import requests
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


since = 0

star_threshold = 1000

github_api_request_counter = 0
algolia_api_request_counter = 0

#startAt = 1008 #FEB 12 2011
startAt = 10654 #MAR 10 2012
stopAt = 20000
counter = 0

#step 1 - Get Links to All Repos
while True:
	#json_entry = [user/repo_name], [# of stars], [username], [dates of mention], {date: # of stars}

	allRepo_URL = 'https://api.github.com/repositories?since=%s' % since
 
	response = requests.get(allRepo_URL, auth=('lvt001@ucsd.edu', 'Vietlong812'))
	github_api_request_counter += 1
	#retrieved the names of the first 100 repositories
	decoded = json.loads(response.text)

	if len(decoded) == 0:
		break

	#step 2 - get # of stars for each repo
	for each_repo in decoded:
		since = each_repo["id"]	#serves to get the last ID so that we pass this into step 1						
		user_repo_name = each_repo["full_name"]
		username = each_repo["owner"]["login"]
		
		repo_URL = 'https://api.github.com/repos/%s' % user_repo_name

		repo_response = requests.get(repo_URL, auth=('lvt001@ucsd.edu', 'Vietlong812'))
		github_api_request_counter += 1
		#retrieved the data about the current state of a repo
		repo_decoded = json.loads(repo_response.text)
		#stars = "N/A"
		stars = 0

		if "stargazers_count" in repo_decoded:
			stars = repo_decoded["stargazers_count"] 
			#step 3 - filter repos for num_stars > star_threshold
			if stars > star_threshold:
				json_entry = [user_repo_name], [stars], [username], [], {}
				print "%s: \t\t\t\t\t\t %s %s." % (user_repo_name, stars, username)

				#step 4 - search HN
				hn_date_of_mention = []

				#each_repo = big_dict[dict_id][0][0]
				hn_incrementor = -1
				each_repo_date_of_mention = []
				while True:
					#print "step 4 while loop entered"
					hn_incrementor += 1
					hn_search_url = 'https://hn.algolia.io/api/v1/search_by_date?query=\"https://github.com/' + user_repo_name + '\"&tags=story&page=' + str(hn_incrementor)
					hn_response = requests.get(hn_search_url)
					algolia_api_request_counter += 1
					#retrieved the HN search results for a particular repo
					hn_decoded = json.loads(hn_response.text)
					if len(hn_decoded["hits"]) == 0:
						break
					for each_hit in hn_decoded["hits"]:
						#print "HN hit Encountered"
						json_entry[3].append(each_hit["created_at"][:10])
						#print json_entry[3]
				#step 5 - Get timeline of number of stars
				print "beginning step 5"
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
				                try:
				                    f = json.load (open ("/Volumes/WD_1TB/GitHub Archive/20"+strYY+"-"+strMM+"-"+strDD+"-"+strHH+".json", 'r') , cls=ConcatJSONDecoder)
				                    for each_event in f:
				                        if(each_event["type"] == "WatchEvent"):
				                            try:
				                                num_stars = int(each_event["repository"]["watchers"])
				                                created_at = each_event["created_at"]
				                                json_entry[4][created_at] = num_stars
				                            except Exception, e:
				                                print e
				                except Exception, e:
				                    print e
				print json_entry[4]
				data = 
				with open('/Volumes/WD_1TB/FinalOutput.json.txt', 'w') as outfile:
  					json.dump(data, outfile)

			else:
				print "below star threhold"
		else:
			print "**IMPORTANT**stargazers_count was not found in repo_decoded"
