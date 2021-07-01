import csv
import random

prob = {}
with open('/home/hduser/1Project/probabilities.csv', 'r+') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for row in reader:
		tmp1 = [float(x) for x in row[2:-1]]
		#1st 2 elements indicate batsman and bowler cluster number, last element is probability of getting out
		tmp2 = [sum(tmp1[0:(i+1)]) for i in range(len(tmp1))]
		#for cumulative probability calculation
		tmp2.append(float(row[-1]))
		prob[(int(row[0]), int(row[1]))] = tuple(tmp2)


batclust = {}
#dictionary indexed by batsman name, value is cluster number
with open('/home/hduser/1Project/batclust.csv', 'r+') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for row in reader:
		batclust[row[0]] = int(row[1])

bowlclust = {}
#dictionary indexed by bowler name, value is cluster number
with open('/home/hduser/1Project/bowlclust.csv', 'r+') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for row in reader:
		bowlclust[row[0]] = int(row[1])

team1 = {'name':'', 'batorder':[], 'bowlorder':[]}
with open('/home/hduser/1Project/team1.csv', 'r+') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	lineno = 0
	for row in reader:
		if lineno == 0:
			team1['name'] = row[0]
		elif lineno == 1:
			team1['batorder'] = row
		elif lineno == 2:
			team1['bowlorder'] = row
		lineno = lineno + 1

team2 = {'name':'', 'batorder':[], 'bowlorder':[]}
with open('/home/hduser/1Project/team2.csv', 'r+') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	lineno = 0
	for row in reader:
		if lineno == 0:
			team2['name'] = row[0]
		elif lineno == 1:
			team2['batorder'] = row
		elif lineno == 2:
			team2['bowlorder'] = row
		lineno = lineno + 1

#team1 batting, team2 bowling first
#initializing opening batsmen
batsman1 = team1['batorder'][0]
batsman2 = team1['batorder'][1]
nextbat = 1
#(nextbat-1) = number of wickets fallen
batsman1cluster = batclust[batsman1] if batsman1 in batclust.keys() else 0
batsman2cluster = batclust[batsman2] if batsman2 in batclust.keys() else 0
batsman1out = 1
batsman2out = 1
#initial probability multiplier = 1

team1score = 0

allout = False

for bowler in team2['bowlorder']:
	bowlercluster = bowlclust[bowler] if bowler in bowlclust.keys() else 0
	pair = (batsman1cluster, bowlercluster)
	#tuple of cluster number of batsman, bowler pair
	for ball in range(6):
		batsman1out = batsman1out * (1 - prob[pair][-1])
		#probability of not getting out this ball
		if batsman1out < 0.5:
			nextbat = nextbat + 1
			if nextbat == 11:
				allout = True
				break
			#replace batsman1 with nextbatsman
			batsman1 = team1['batorder'][nextbat]
			batsman1cluster = batclust[batsman1] if batsman1 in batclust.keys() else 0
			batsman1out = 1
			continue
		r = random.random()
		runs = 0
		for i in range(len(prob[pair])):
			if r <= prob[pair][i]:			
				runs = i
				break
				#find range in which random number falls, range will be = runs scored
		team1score += runs
		if runs in (1,3):
			#when 1 or 3 runs are scored, batsmen exchange strike
			(batsman1, batsman2) = (batsman2, batsman1)
			(batsman1cluster, batsman2cluster) = (batsman2cluster, batsman1cluster)
			(batsman1out, batsman2out) = (batsman2out, batsman1out)
	if allout:
		break
	#end of over, batsmen exchange strike
	(batsman1, batsman2) = (batsman2, batsman1)
	(batsman1cluster, batsman2cluster) = (batsman2cluster, batsman1cluster)
	(batsman1out, batsman2out) = (batsman2out, batsman1out)

print "1st Innings:\n", team1['name'], "Score: ", team1score, "/", (nextbat-1)

#same algorithm, for team2 batting and team1 bowling
batsman1 = team2['batorder'][0]
batsman2 = team2['batorder'][1]
nextbat = 1
batsman1cluster = batclust[batsman1] if batsman1 in batclust.keys() else 0
batsman2cluster = batclust[batsman2] if batsman1 in batclust.keys() else 0
batsman1out = 1
batsman2out = 1

team2score = 0

allout = False

for bowler in team1['bowlorder']:
	bowlercluster = bowlclust[bowler] if bowler in bowlclust.keys() else 0
	pair = (batsman1cluster, bowlercluster)
	for ball in range(6):
		batsman1out = batsman1out * (1 - prob[pair][-1])
		if batsman1out < 0.5:
			nextbat = nextbat + 1
			if nextbat == 11:
				allout = True
				break
			batsman1 = team2['batorder'][nextbat]
			batsman1cluster = batclust[batsman1] if batsman1 in batclust.keys() else 0
			batsman1out = 1
			continue
		r = random.random()
		runs = 0
		for i in range(len(prob[pair])):
			if r <= prob[pair][i]:			
				runs = i
				break
		team2score += runs
		if runs in (1,3):
			(batsman1, batsman2) = (batsman2, batsman1)
			(batsman1cluster, batsman2cluster) = (batsman2cluster, batsman1cluster)
			(batsman1out, batsman2out) = (batsman2out, batsman1out)
	if allout:
		break
	(batsman1, batsman2) = (batsman2, batsman1)
	(batsman1cluster, batsman2cluster) = (batsman2cluster, batsman1cluster)
	(batsman1out, batsman2out) = (batsman2out, batsman1out)

print "2nd Innings:\n", team2['name'], "Score: ", team2score, "/", (nextbat-1)

#winner is the team who scored more runs
print "Winner: ", team1['name'] if team1score > team2score else team2['name']
