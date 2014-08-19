Correlating Hacker News Upvotes and GitHub Stars
3rd Annual GitHub Data Challenge

With this data analysis we aim to answer a simple question: "How does posting a link to my repository on HackerNews change the number of stars my repository has?"
To skip to the conclusion, click here now.
I will briefly go over the methods employed to draw the conclusion followed by an explanation of the results.

The task of obtaining an answer to my research question can be thought of in 3 steps: 1. Obtain the data 2. Analyze the Data 3. Visualize the analysis

Step 1 - Obtaining the Data:

Description: The task here was to obtain the entire history of GitHub events to create a timeline of each repository's history

Challenge: Every data source GitHub provided had its own challenges. Originally I tried using the GitHub API's timeline of events. I eventually determined that it was not possible to get all the data I would have liked due to pagination limitations. My next attempt was to try and use Google BigQuery. This technology impressed me like no other, but unfortunately the analysis I wanted to complete could not be done for free. The next option for me was to use the GitHub Archive. The problem with this method was that I could not find a Python GZIP reader that could handle the files I downloaded. 

Solution: I found a Ruby script that could handle downloading and reading the data. I used this to download XX,XXX files and extract the data into .json files. See downloadAllData.rb


Challenge: Reading the newly created JSON data. The data downloaded and written was in a form I've seen referenced as a JSON stream. Standard Python libraries could not handle this.

Solution: I used a SO user's class for reading the json file and performing analysis.


Challenge: Analyzing the data - I quickly realized that the data could not be analyzed in this form due to time cost. It was taking over 5 hours to query information about a single repository. 

Solution: MySQL DB - I used the python script to read the data and insert the relevant* data into a MySQL db. This took approximately 7.5 hours


Challenge: Limiting the scope of data analyzed - There were over 17million entries in my event_table and I couldn't analyze all of these. I wanted to limit the scope to analyze repositories only with currently greater than X stars. 

Solution: I used a SO user's solution to write the query. The link to it can be found here. This proved to be a challenging and expensive query to run. This got me a table called max_stars


Challenge: Obtaining the HN Data - Now that I had the names of the repositories I wanted to look up on HN, I needed to query HN for the data.

Solution: I used the HN Algolia API. This was a pretty straight forward process.


Challenge: Limit the scope of HN Data - I had a bunch of HN events, but I realized that most people had duplicate posts. Only one post for each person got a significant number of upvotes and as such I only wanted to include the "relevant" HN posts

Solution: Luckily I already had a query that looked similar - The one I used for limiting the GitHub data!


Challenge: 







Order of Files Used:

downloadAllData.rb 			-	download all of the data into json files
JSONtoMySQL.py 				- 	transfer relevant JSON data to a MySQL database
searchDBForCurrentStars.py 	- 	is reponsible for getting the most recent entry for each repository
getHNData.py 				-	query the algolia API to get the hn data into DB (55 hours to run)
hnTabletoHNTableMax.py		- 	gets the most relevant HN event for each repo
getRelevantGHevents.py 		- 	gets the most relevant GH events based on HN mentions
analyzeData.py 				- 	Analyzes the data and saves results into DB
graph.py 					-	This file prepares the HTML for graphing






The HackerNews Bump
Correlating GitHub Stars with Hacker News Upvotes
3rd Annual GitHub Data Challenge

With this data analysis we aim to answer the question: "How does posting a link to a repository on HackerNews change the number of stars a repository has?"
Or more generally, "Is there such thing as the HN Bump?"


The short answer to this question is that it will _____ the rate of growth in number of stars for the repo by ____%. The percentage increase varies depending on the number of stars your repository has and the number of upvotes your HackerNews post has.

Insert main graph here


Caption: This graph shows a series of things. First, it constrains the data to only match what is selected by the sliders. In red it shows the daily % increase in the number of stars for the week before and after a HN mention. In blue it shows the daily % increase in the number of stars for all repositories in the week surrounding the date we expect a mention to happen.

That was a mighty caption so let us break down what it means and why we are using this data. First there are the two sliders you see up above. One controls the number of stars, and one controls the number of HN Points. These constrain the data represented in the graph to tiers. The reason for this is that there exists a big disparity in the effects on a repository with 50,000 stars as compared to one with less than 50 stars. The HN constraint is to help determine the number of HN Points you need your repository to get for it to get you the "bump". It is important to note that the GitHub repositories without mentions on hacker news (see blue) are not constrained by the HN_points slider.

Now that we have covered the sliders, lets go over to the red data source. The blue line represents the percdenage increase in the number of stars each day. This is calculated by looking at the number of stars on each day for an individual repository, comparing it to the number of stars for the previous day, and calculating a percent increase. The data was calculated this way because we found the data to be too far skewed in the direction of large repositories when looking at raw increase in number of stars. If you want to see that chart, see below.

The next data source we have is the all important baseline blue data. This contains has the information about all GitHub repositories within the constraints. It serves the purpose of showing us the daily rate of increase in stars we should expect a GitHub repository to have. This is useful in determining whether HN has any effect at all. The data included here is not the 14 day outlook for every span of days for every repository. It instead looks to our red data source to determine the number of days after a repository has been created for its HN feature [1]. We then use the 14 days surrounding the expected_hn_mention date to calculate our data. The reason we use this date is because to maintain the integrity of the estimate, the number of days after the repository's creation must be held constant.

This is essentially how we got our data! For more in depth information about the techniques used in calculation, methods, challenges, code, steps for recreation and insights check out this blog post!

The data was acquired from the GitHub Archive, the GitHub API, and the Algolia HN Api.

Thanks for reading! We welcome any feedback you may have!





---
We determined the average number of days after a repository's creation to expect a HN mention. This value was calculated for each point and star threshold, but in the end the differences in the number of days seemed arbitrary and patternless. Therefore, we chose the average of these values to come up with: If a repository is mentioned on HN it is on average 352 after it's creation.
This conclusion was used in the next step to analyze the data. We wanted to use data from events between 345 and 359 days after a repository was created. This was the closest approximation to a HN event and therefore closest to the range we used for the other calculation. In here lies a potential source of error for our baseline calculation. HN_events represent a popularity surge for repositories as seen in thr graphs. For the baseline, the arbitray 352 days after a repository's creation has no such growth and it is therefore difficult to obtain data for the expected growth at that time. Where as this may be an error in computing the conclusion to the question of how much it aids growth, it may answer the question of "does HN help a repository stay relevant a year after it's creation." The answer to that the data clearly shows to be yes. 

---
Instead of using a specific 352 days after a repository has been created, how about using a larger scope of data. Look for all events relating to a specific repo and look for the longest period of consecutive days of growth. If that value exceeds 5, use that growth. The problem with this is that it is only using days where we know there to be growth. Compare this to HN where we have no expectation of growth. It is a fortunate outcome for some, but not all, repositories. 
