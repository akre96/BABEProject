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
def beam(BB_File):
	# Opening Beam Break File


	txt = open(BB_File)

	#Reading as a csv file
	csvFile = csv.reader(txt, delimiter='\t');


	#Creating list of dates as datetime objects
	perHour = []
	perDay = []
	for row in csvFile:
		year = int(row[0])
		month = int(row[1])
		day = int(row[2])
		hour = int(row[3])
		minute = int(row[4])
		second = int(row[5])

		perDay.append(datetime(year, month, day)) #BB only ocunting days
		perHour.append(datetime(year, month, day,hour)) #BB per hour

#	perHour = {z:perHour.count(z) for z in perHour}
#	perHour = sorted(perHour.items())
	
	#Finding average uses per day
	perDay = {z:perDay.count(z)/5 for z in perDay}
	perDay = sorted(perDay.items())
	averagePerDay = np.mean([item[1] for item in perDay])   

	#making indexes for per hour and per day
#	indexHour = np.arange(len(perHour))
	indexDay = np.arange(len(perDay))

	#return the date entries, per day list, and average per day number
	return perDay, averagePerDay, indexDay