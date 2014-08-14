import MySQLdb

db = MySQLdb.connect(host="localhost", # your host, usually localhost
	                     user="root", # your username
	                      passwd="password", # your password
	                      db="githubDB") # name of the data base

cur = db.cursor() 

cur.execute("SELECT * FROM chart_table_three WHERE slider_hn_points = 500 AND slider_stars = 10")
graph_data = cur.fetchall()


before = '<html>\n<head>\n<script type=\"text/javascript\" src=\"https://www.google.com/jsapi\"></script>\n<script type=\"text/javascript\">\ngoogle.load(\'visualization\', \'1\', {packages: [\'corechart\']});\ngoogle.setOnLoadCallback(drawVisualization);\nfunction drawVisualization() {\nvar data = new google.visualization.DataTable();\ndata.addColumn(\'string\', \'x\');\ndata.addColumn({type: \'string\', role: \'annotation\'});\ndata.addColumn({type: \'string\', role: \'annotationText\'});'
add_col = ''
repo_count = 0
count = 0
for data in graph_data:
	repo_count += 1
	if repo_count == 15:
		add_col += "data.addColumn('number', '%s');" % count 
		count += 1
		repo_count = 0

day_list = [''] * 15 
day_list[0] = 'data.addRow(["-7", null, null'
day_list[1] = 'data.addRow(["-6", null, null'
day_list[2] = 'data.addRow(["-5", null, null'
day_list[3] = 'data.addRow(["-4", null, null'
day_list[4] = 'data.addRow(["-3", null, null'
day_list[5] = 'data.addRow(["-2", null, null'
day_list[6] = 'data.addRow(["-1", null, null'
day_list[7] = 'data.addRow(["0", \'HN\', \'Hacker News Bump\''
day_list[8] = 'data.addRow(["1", null, null'
day_list[9] = 'data.addRow(["2", null, null'
day_list[10] = 'data.addRow(["3", null, null'
day_list[11] = 'data.addRow(["4", null, null'
day_list[12] = 'data.addRow(["5", null, null'
day_list[13] = 'data.addRow(["6", null, null'
day_list[14] = 'data.addRow(["7", null, null'

add_row = ''
i = 0
prev = 0
for data in graph_data:
	prev = data[4]
	if i == 11:
		prev = 0.5
	
	day_list[i] += ', %s' % prev
	i += 1
	if i == 15:
		i = 0

for day in day_list:
	day += ']);'
	add_row += day

after = '\nnew google.visualization.LineChart(document.getElementById(\'visualization\')).draw(data,\n{width:1000,height:800,vAxis:\n{maxValue:10},annotations:\n{style:\'line\'}});}\n</script>\n</head>\n<body><div id="visualization">\n</div>\n</body>\n</html>'

print before
print add_col
print add_row
print after