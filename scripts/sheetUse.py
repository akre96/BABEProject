#SHEET USE
#
# Summary: Analyse data from manually logged lactation room usage sheets.
#
# Input: file path to csv of manually logged lactation room usage
# Output: -averageDict: a dictionary who's keys are room numbers 
#			and values are average use per day for that room.

import csv
from datetime import datetime
import numpy as np
import operator

def sheetUse(Usage_Sheet):
	# Opening usage File
	roomNums = []
	txt = open(Usage_Sheet)
	rooms = dict()

	#Reading as a csv file
	csvFile = csv.reader(txt);
	roomDate = []

	for row in csvFile:
		#Find room number accounting for errors in data sheet ('rr' is last letters of Kerr assigned to room 15)
		number = row[5][-2:].strip()
		if number == 'rr':
			number = '15'

		#formatting entry date in datetime
		dateRaw = row[1]
		date = datetime.strptime(dateRaw,"%m/%d/%Y")

		roomDate.append([int(number),date])
		roomNums.append(int(number))
	#Finding unique rooms logged
	roomNums = set(roomNums)
	roomDict={}

	#For each unique room finds dates associated with it and appends in a dictionary
	for x in roomNums:
		for y in roomDate:
			if y[0] == x:
				try:
					roomDict[x].append(y[1])
				except(KeyError):
					roomDict[x]=[y[1]]
	averageDict = {}
	for key,value in roomDict.iteritems():
			#perDay = {z:perDay.count(z)/5 for z in perDay}
			#perDay = sorted(perDay.items())
		perDay = {z:value.count(z) for z in value}
		perDay = sorted(perDay.items())
		averagePerDay = np.mean([item[1] for item in perDay])

		averageDict[key] = averagePerDay
	sortRooms = sorted(averageDict.keys())
	sortAvg = [averageDict[x] for x in sortRooms]
		
	return sortRooms, sortAvg
