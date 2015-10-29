	## BEAM BREAK

import csv
from datetime import datetime
import numpy as np
def beam(BB_File):
	# Opening Beam Break File


	txt = open(BB_File)

	#Reading as a csv file
	csvFile = csv.reader(txt, delimiter='\t');


	#Creating list of dates as datetime objects
	date = []
	perDay = []
	for row in csvFile:
		year = int(row[0])
		month = int(row[1])
		day = int(row[2])
		hour = int(row[3])
		minute = int(row[4])
		second = int(row[5])

		perDay.append(datetime(year, month, day)) #BB only ocunting days
		date.append(datetime(year, month, day,hour)) #BB per hour


	#Finding average uses per day
	perDay = {z:perDay.count(z)/2 for z in perDay}
	averagePerDay = np.mean(perDay.values())


	#return the date entries, per day list, and average per day number
	return date, perDay, averagePerDay