Correlating Hacker News Upvotes and GitHub Stars
3rd Annual GitHub Data Challenge

With this data analysis we aim to answer a simple question: "How does posting a link to my repository on HackerNews change the number of stars my repository has?"
To skip to the conclusion, click here now.
I will briefly go over the methods employed to draw the conclusion followed by an explanation of the results.

The task of obtaining an answer to my research question can be thought of in 3 steps: 1. Obtain the data 2. Analyze the Data 3. Visualize the analysis

Step 1 - Obtaining the Data:

Description: The task here was to obtain the entire history of GitHub events to create a timeline of each repository's history

Challenge: Every data source GitHub provided had its own challenges. Originally I tried using the GitHub API's timeline of events. I eventually determined that it was not possible to get all the data I would have liked due to pagination limitations. My next attempt was to try and use Google BigQuery. This technology impressed me like no other, but unfortunately the analysis I wanted to complete could not be done for free. The next option for me was to use the GitHub Archive. The problem with this method was that I could not find a Python GZIP reader that could handle the files I downloaded. 

Solution: I found a Ruby script that could handle downloading and reading the data. I used this to download XX,XXX files and extract the data into .json files. 


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