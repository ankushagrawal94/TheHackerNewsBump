#The HackerNews Bump
##Correlating GitHub Stars with Hacker News Upvotes##
----------

With this data analysis we aim to answer the question: *"How does posting a link to a repository on HackerNews change the number of stars a repository has?"*
Or more generally, *"Is there such thing as the HN Bump?"*


The short answer to this question is that it will increase the rate of growth in number of stars for the repo by an average of 38.16% from -0.71% to 37.45%. The percentage increase varies depending on the number of stars your repository has and the number of upvotes your HackerNews post has.

To see the behaviour of daily percentage growth each day, try working with the graph below. This graph is the result of 17 million events from April 2012- August 2014.


Insert main graph here


Caption: This graph shows a series of things. First, it constrains the data to only match what is selected by the sliders. In red it shows the daily % increase in the number of stars for the week before and after a HN mention. In green it shows the daily % increase in the number of stars for all repositories in the week surrounding the date we expect a mention to happen.

That was a mighty caption so let us break down what it means and why we are using this data. First there are the two sliders you see up above. One controls the number of stars, and one controls the number of HN Points. These constrain the data represented in the graph to tiers. The reason for this is that there exists a big disparity in the effects on a repository with 50,000 stars as compared to one with less than 50 stars. The HN constraint is to help determine the number of HN Points you need your repository to get for it to get you the "bump". It is important to note that the GitHub repositories without mentions on hacker news (see green) are not constrained by the HN_points slider.

Now that we have covered the sliders, lets go over to the red data source. The green line represents the percentage increase in the number of stars each day. This is calculated by looking at the number of stars on each day for an individual repository, comparing it to the number of stars for the previous day, and calculating a percent increase. The data was calculated this way because we found the data to be too far skewed in the direction of large repositories when looking at raw increase in number of stars. If you want to see that chart, see below.

The next data source we have is the all important baseline green data. This contains has the information about all GitHub repositories within the constraints. It serves the purpose of showing us the daily rate of increase in stars we should expect a GitHub repository to have. This is useful in determining whether HN has any effect at all. The data included here is not the 14 day outlook for every span of days for every repository. It instead looks to our red data source to determine the number of days after a repository has been created for its HN feature [1]. We then use the 14 days surrounding the expected_hn_mention date to calculate our data. The reason we use this date is because to maintain the integrity of the estimate, the number of days after the repository's creation must be held constant.

This is essentially how we got our data! For more in depth information about the techniques used in calculation, methods, challenges, code, steps for recreation and insights check out this blog post!

The data was acquired from the GitHub Archive, the GitHub API, and the Algolia HN Api.

Thanks for reading! We welcome any feedback you may have!

----------

Order of Files Used:
```
 - downloadAllData.rb 				-	download all of the data into JSON files
 - JSONtoMySQL.py 					- 	transfer relevant JSON data to a MySQL  - database
 - searchDBForCurrentStars.py 		- 	is responsible for getting the most recent entry for each repository
 - getHNData.py 					-	query the algolia API to get the hn data into DB (55 hours to run)
 - hnTabletoHNTableMax.py			- 	gets the most relevant HN event for each repo
 - getRelevantGHevents.py 			- 	gets the most relevant GH events based on HN mentions
 - getExpectedDateOfMention.py 		- 	gets the hn_expected_date_of_mention
 - getRelevantGHeventAvgCase.py 	-	get the GH events within 1 week of the hn_expected_date_of_mention
 - analyzeData.py 					- 	Analyzes the data and saves results into DB
 - analyzeDateAvgCase.py 			-	Analyzes the average cases data
 - graph.py 						-	This file prepares the HTML for graphing
 - get_chart_table.py 				-	Prepares the data that will be pasted into google spreadsheet
```

##Tables Used

chart_table_avg
```
+------------------+--------------+------+-----+---------+-------+
| Field            | Type         | Null | Key | Default | Extra |
+------------------+--------------+------+-----+---------+-------+
| day              | int(6)       | YES  |     | NULL    |       |
| slider_stars     | int(6)       | YES  |     | NULL    |       |
| slider_hn_points | int(6)       | YES  |     | NULL    |       |
| daily_avg_stars  | int(8)       | YES  |     | NULL    |       |
| daily_growth     | double(10,5) | YES  |     | NULL    |       |
| change_in_growth | double(10,5) | YES  |     | NULL    |       |
| num_data_points  | int(6)       | YES  |     | NULL    |       |
+------------------+--------------+------+-----+---------+-------+
```
chart_table
```
+-------------------+--------------+------+-----+---------+-------+
| Field             | Type         | Null | Key | Default | Extra |
+-------------------+--------------+------+-----+---------+-------+
| day               | int(6)       | YES  |     | NULL    |       |
| slider_stars      | int(6)       | YES  |     | NULL    |       |
| slider_hn_points  | int(6)       | YES  |     | NULL    |       |
| daily_total_stars | int(8)       | YES  |     | NULL    |       |
| daily_growth      | double(10,5) | YES  |     | NULL    |       |
| change_in_growth  | double(10,5) | YES  |     | NULL    |       |
+-------------------+--------------+------+-----+---------+-------+
```
days_after
```
+-----------------+--------+------+-----+---------+-------+
| Field           | Type   | Null | Key | Default | Extra |
+-----------------+--------+------+-----+---------+-------+
| stars           | int(6) | YES  |     | NULL    |       |
| hn_points       | int(6) | YES  |     | NULL    |       |
| avg_days_after  | int(6) | YES  |     | NULL    |       |
| mode_days_after | int(6) | YES  |     | NULL    |       |
| num_data_points | int(6) | YES  |     | NULL    |       |
+-----------------+--------+------+-----+---------+-------+
```
event_table_two
```
+--------------+--------------+------+-----+---------+-------+
| Field        | Type         | Null | Key | Default | Extra |
+--------------+--------------+------+-----+---------+-------+
| repo_name    | varchar(255) | YES  |     | NULL    |       |
| stars        | int(6)       | YES  |     | NULL    |       |
| event_time   | date         | YES  |     | NULL    |       |
| repo_created | date         | YES  |     | NULL    |       |
+--------------+--------------+------+-----+---------+-------+
```
event_table_condensed 
```
+------------+--------------+------+-----+---------+-------+
| Field      | Type         | Null | Key | Default | Extra |
+------------+--------------+------+-----+---------+-------+
| repo_name  | varchar(255) | YES  |     | NULL    |       |
| stars      | int(6)       | YES  |     | NULL    |       |
| event_time | date         | YES  |     | NULL    |       |
+------------+--------------+------+-----+---------+-------+
```
event_table_general_condensed
```
+--------------+--------------+------+-----+---------+-------+
| Field        | Type         | Null | Key | Default | Extra |
+--------------+--------------+------+-----+---------+-------+
| repo_name    | varchar(255) | YES  |     | NULL    |       |
| stars        | int(6)       | YES  |     | NULL    |       |
| event_time   | date         | YES  |     | NULL    |       |
| repo_created | date         | YES  |     | NULL    |       |
+--------------+--------------+------+-----+---------+-------+
```
hn_event_max
```
+------------+--------------+------+-----+---------+-------+
| Field      | Type         | Null | Key | Default | Extra |
+------------+--------------+------+-----+---------+-------+
| repo_name  | varchar(255) | YES  |     | NULL    |       |
| stars      | int(6)       | YES  |     | NULL    |       |
| hn_points  | int(6)       | YES  |     | NULL    |       |
| event_time | date         | YES  |     | NULL    |       |
+------------+--------------+------+-----+---------+-------+
```
hn_event_table_two
```
+------------+--------------+------+-----+---------+-------+
| Field      | Type         | Null | Key | Default | Extra |
+------------+--------------+------+-----+---------+-------+
| repo_name  | varchar(255) | YES  |     | NULL    |       |
| stars      | int(6)       | YES  |     | NULL    |       |
| hn_points  | int(6)       | YES  |     | NULL    |       |
| event_time | date         | YES  |     | NULL    |       |
+------------+--------------+------+-----+---------+-------+
```
latest_repo_events
```
+------------+--------------+------+-----+---------+-------+
| Field      | Type         | Null | Key | Default | Extra |
+------------+--------------+------+-----+---------+-------+
| repo_name  | varchar(255) | YES  |     | NULL    |       |
| stars      | int(6)       | YES  |     | NULL    |       |
| hn_points  | int(6)       | YES  |     | NULL    |       |
| event_time | date         | YES  |     | NULL    |       |
+------------+--------------+------+-----+---------+-------+
```
max_stars
```
+------------+--------------+------+-----+---------+-------+
| Field      | Type         | Null | Key | Default | Extra |
+------------+--------------+------+-----+---------+-------+
| repo_name  | varchar(255) | YES  |     | NULL    |       |
| stars      | int(6)       | YES  |     | NULL    |       |
| event_time | date         | YES  |     | NULL    |       |
+------------+--------------+------+-----+---------+-------+
```