## BEAM BREAK
# Summary: Analyses data of a single beam break file.
#
#	Input: Path to a csv file containing beam break data
#	Output: 
#		-perDay: Array of room uses per day of recorded data
#		-averagePerDay: float of average uses of room per day
#		-indexDay: An indexing array the length of perDay

import csv
from datetime import datetime
import numpy as np
def beam(BB_File,dayTime=True,weekDay=True):

	# Opening Beam Break File


	txt = open(BB_File)

	#Reading as a csv file
	csvFile = csv.reader(txt, delimiter='\t');


	#Creating list of dates as datetime objects
	perHour = []
	perDay = []
	for row in csvFile:
		year = 2000+int(row[0])
		month = int(row[1])
		day = int(row[2])
		hour = int(row[3])
		minute = int(row[4])
		second = int(row[5])
		if (year == 2015 and month >= 11): 
			if dayTime:
				if hour >= 8 and hour <=21:
					perDay.append(datetime(year, month, day))
			else:
				perDay.append(datetime(year, month, day)) #BB only ocunting days
#				perHour.append(datetime(year, month, day,hour)) #BB per hour


	
	#Finding average uses per day
	if weekDay:
		perDay = {z:perDay.count(z)/5 for z in perDay if z.weekday() < 5}
	else:
		perDay = {z:perDay.count(z)/5 for z in perDay}

	perDay = sorted(perDay.items())
	dateRange = perDay[-1][0] - perDay[0][0]
	dRange = (dateRange.days)
	if (dRange > 0):
		averagePerDay = (np.sum([item[1] for item in perDay])/dRange) * (7/5)
	else:
		averagePerDay = 0

	#making indexes for per hour and per day
	indexDay = np.arange(len(perDay))

	#return the date entries, per day list, and average per day number
	return perDay, averagePerDay, indexDay