##TEMPERATURE AND HUMIDITY
#
# Summary:
#
# Input: Path to a csv file containing temperature and humidity data
# Output: 
#	- date: Array of dates when data was collected
#	- tempData: Dictionary containing an array of temperatures for each date,
#		and several other analysis of the temperature
#	- humData: Dictionary containing an array of humidity for each date, and
#		several other analysis of the humidity

import csv
from datetime import datetime
import numpy as np




## TEMPERATURE AND HUMIDITY
def tempHum(TH_File):
	txt = open(TH_File)

	#Reading as a csv file
	csvFile = csv.reader(txt, delimiter='\t');


	#Creating list of dates as datetime objects
	date = []
	th = []
	for row in csvFile:
		year = int(row[0])
		year = 2000+year
		month = int(row[1])
		day = int(row[2])
		hour = int(row[3])
		minute = int(row[4])
		second = int(row[5])
		temp = float(row[6])
		hum = float(row[7])
		if year == 2015 and month >= 11: 
			date.append(datetime(year, month, day,hour,minute,second))
			th.append([temp,hum])
	th = np.array(th)


	tempIndex = (Ellipsis,0)
	tempList = th[tempIndex]

	humIndex = (Ellipsis,1)
	humList = th[humIndex]

	#finding average values
	tempMean = np.mean(tempList)
	humMean = np.mean(humList)

	#finding variance
	tempVar = np.var(tempList)
	humVar = np.var(humList)

	#finding min and max
	tempMax = max(tempList)
	humMax = max(humList)

	tempMin = min(tempList)
	humMin = min(humList)

	#finding humidity <60 or >90
	lowHumInd = []
	highHumInd = []
	for index, hum in enumerate(humList):
		if hum <= 60:
			lowHumInd.append(index)
		if hum >= 90:
			highHumInd.append(index)

	timeBelowSixty= len(lowHumInd)*15 #in minutes
	timeAboveNinety = len(highHumInd)*15


	tempData = {
		'list':tempList,
		'mean':tempMean,
		'var':tempVar,
		'max':tempMax,
		'min':tempMin,
		}
	humData = {
		'list':humList,
		'mean':humMean,
		'var':humVar,
		'max':humMax,
		'min':humMin,
		'belowSixty':timeBelowSixty,
		'aboveNinety':timeAboveNinety,

		}

	return date, tempData, humData
