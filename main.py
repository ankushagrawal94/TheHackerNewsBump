import requests
import json

big_dict = {}

since = 0

#step 1
starThreshold = 1000

requestCounter = 0
algolia_request_counter = 0
while True:

	allRepo_URL = 'https://api.github.com/repositories?since=%s' % since
 
	response = requests.get(allRepo_URL, auth=('lvt001@ucsd.edu', 'Vietlong812'))
	decoded = json.loads(response.text)
	requestCounter += 1
	list_of_id = []
	list_of_repos = []
	list_of_num_stars = []
	list_of_user_name = []

	if len(decoded) == 0:
		break
	#step 2
	for eachDecoded in decoded:
		ID = eachDecoded["id"]								
		repo_name = eachDecoded["full_name"]
		username = eachDecoded["owner"]["login"]

		#repo_dict = ('ID KEY' : ["url", "# of stars", "# of mentions", ['List of dates mentioned']]])

		repo_URL = 'https://api.github.com/repos/%s' % repo_name

		repo_response = requests.get(repo_URL, auth=('lvt001@ucsd.edu', 'Vietlong812'))
		repo_decoded = json.loads(repo_response.text)
		requestCounter += 1
		stars = 'N/A'

		if "stargazers_count" in repo_decoded:
			stars = repo_decoded["stargazers_count"] 
			#step 3
			if stars > starThreshold:
				big_dict[ID] = [repo_name], [stars], [username], [], {}
				#f = open ('/Development/GitHubChallenge/text.txt', 'w')
				#f.write (str(big_dict))
				#f.close()
				#print "wrote to file"
				#list_of_id.append(ID)
				#list_of_repos.append(repo_name)
				#list_of_num_stars.append(stars)
				#list_of_user_name.append(username)
				#print "%s: %s \t\t\t\t\t\t %s %s." % (ID, repo_name, stars, username)
				print big_dict[ID]
		since = ID

	#Step 4
	hn_date_of_mention = []
	for dict_id in big_dict:
		print "step 4 for loop entered"
		each_repo = big_dict[dict_id][0][0]
		hn_incrementor = -1
		each_repo_date_of_mention = []
		while True:
			print "step 4 while loop entered"
			hn_incrementor += 1
			hn_search_url = 'https://hn.algolia.io/api/v1/search_by_date?query=' + each_repo + '&tags=story&page=' + str(hn_incrementor)
			hn_response = requests.get(hn_search_url)
			hn_decoded = json.loads(hn_response.text)
			algolia_request_counter += 1
			if len(hn_decoded["hits"]) == 0:
				break
			for each_hit in hn_decoded["hits"]:
				each_repo_date_of_mention.append(each_hit["created_at"])
			big_dict[dict_id][3].append(each_repo_date_of_mention)
			print "algolia_request_counter is: "
			print algolia_request_counter
		if len(big_dict[dict_id][3]) == 0:
			print ""
		#	del big_dict[dict_id]
		else:
			#step 5
			incrementer = -1
			stars_per_day_dict = {}
			new_url = ""
			while True:
				print "step 5 while loop entered"
				incrementer += 1
				getEventsParams = {'page': incrementer}
				url = 'https://api.github.com/users/'+big_dict[dict_id][2][0]+'/received_events'
				r = requests.get(url)
				requestCounter += 1
				#if len(new_url) == 0:
				#	r = requests.get(url, params=getEventsParams)
				#else:
				#	r = requests.get(new_url)
				#head = requests.head(url = r.url)
				#print r.url
				#print head.links
				#print head.links["next"]
				#print head.links["next"]["url"]
				#new_url = head.links["next"]["url"]
				decoded = json.loads(r.text)
				date_parsed = ""
				num_stars_day = 0
				if len(decoded) == 0:
					print "decoded over"
					break
				if "documentation_url" in decoded:
					print "page limit exceeded"
					break
				for x in decoded:
					event_type =  x["type"]
					repo_acted_on = x["repo"]["name"]
					created_at_date = x["created_at"][:10]
					
					if event_type == "WatchEvent" and repo_acted_on == big_dict[dict_id][0]:
						if date_parsed != created_at_date:
							num_stars_day = 1
							date_parsed = created_at_date
						else:
							num_stars_day += 1
						big_dict[dict_id][4][date_parsed] = num_stars_day
		print "\n\n\n\n"
		print(big_dict)

		f = open ('/Development/GitHubChallenge/text2.txt', 'w')
		f.write (str(big_dict))
		f.close()
		print "GitHub Request Counter is: "
		print requestCounter
		print "algolia_request_counter is: "
		print algolia_request_counter
		print "finished one iteration of main while loop"
