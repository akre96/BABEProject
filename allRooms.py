# This script is intended to analyze all the rooms which have data
import os
import argparse
import glob
import numpy as np
from scripts.tempHum import tempHum
from scripts.beam import beam
from scripts.sheetUse import sheetUse
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime



#Adding support for command line arguments
parser = argparse.ArgumentParser(description='Process Data from all rooms')
parser.add_argument('-log', '-l', action='store_const',const=1,help='Stops analysis from manual log in sheet')
parser.add_argument('-day','-d', action='store_const',const=1, help='Stops filtering beambreak data from 8am-10pm')
parser.add_argument('-week','-w', action='store_const',const=1, help='Stops filtering beambreak data for only weekdays')
args = parser.parse_args()

#establish path to file in order to analyze data
currentDir = os.getcwd() +'/data/room'

meanTemp=[]
meanHum=[]
averageBB = []
notWorking = []
roomIndex=[]
noData=[]
roomDict={}
day = True
week = True

#iterate through each room and collect temp, hum, and beam break data

for room in [f for f in os.listdir(currentDir) if not f.startswith('.')]:
	currentRoom = currentDir+"/"+room
    #Check if data in the rooms folder
	if os.listdir(currentRoom):
	#Checks to see if any exceptions raised because no TH data in and ahead of 11/2015
		try:
			roomBB = glob.glob(currentRoom+'/BB*')
			roomTH = glob.glob(currentRoom+'/TH*')
			thDates, tempData, humData = tempHum(roomTH[0])

			if (tempData['mean'] and humData['mean']):

				meanTemp.append(tempData['mean'])
				meanHum.append(humData['mean'])

				if args.day == 1:
					day = False
				if args.week == 1:
					week = False
				perDay, averagePerDay, indexDay = beam(roomBB[0],dayTime = day, weekDay = week)
			
				roomDict[int(room)] = averagePerDay
				averageBB.append(averagePerDay)

				roomIndex.append(room)
			else:
				notWorking.append(room)

		except IndexError:
			notWorking.append(room)
	else:
		noData.append(room)


responseSheet = os.getcwd() + '/data/other/responses.csv'
sheetRooms, sheetAverage, sheetDict = sheetUse(responseSheet)


notWorking.sort()
print "Average temperature: %.2f C" % np.mean(meanTemp)
print "Average usage per day: %.2f" % np.mean(averageBB)
print "Rooms without data past 11/1/2015: "+' '.join(str(x) for x in notWorking)

roomIndex = sorted(roomDict.keys())
averageBB = [roomDict[x] for x in roomIndex]

roomNum = list(xrange(len(averageBB)))
sheetBB = list(xrange(len(sheetAverage)))

combinedRooms = []
combinedSensor = []
combinedSheet = []
for x in sheetRooms:
	if (x in roomDict):
		combinedRooms.append(x);
		combinedSensor.append(roomDict[x])
		combinedSheet.append(sheetDict[x])


#Save each graph as a page of a PDF file with current date as title
d = datetime.today()
d = d.strftime("%m-%d-%Y")
flag=""
if args.log == 1:
	flag =flag+ 'NoSheet_'

if (args.day == 1):
	flag = flag+'allDay'

if args.week == 1:
	flag = flag + 'allWeek'



graphLoc = "graphs/AllRooms_"+flag+d+".pdf"


with PdfPages(graphLoc) as pdf:
	#Figure 1 displays with optional -l argument
	#Figure 1 contains the average uses per day from Beam break vs the uses recorded on lactation room sign in sheet
	if (args.log != 1):
		ind = np.arange(len(combinedRooms))
		width = 0.4

		fig, ax = plt.subplots()
		rects1 = ax.bar(ind, combinedSensor, width, color='r')
		rects2 = ax.bar(ind + width, combinedSheet, width, color='y')


		ax.set_ylabel('Room Usage')
		ax.set_title('Lactation room usage')
		ax.set_xticks(ind + width)
		ax.set_xticklabels(combinedRooms)

		ax.legend((rects1[0], rects2[0]), ('Sensor', 'Log-in Sheet'))
		pdf.savefig()
		plt.close()



	fig1 = plt.figure()
	bb = fig1.add_subplot(1,1,1)
	x1 = bb.bar(roomNum,averageBB, align = "center", color = "g")
	plt.title("Average Uses per Day by Beam Break")
	plt.xticks(roomNum,roomIndex)
	bb.set_ylabel('Uses')
	bb.set_xlabel('Room')
	swags = bb.patches
	for swag, value in zip(swags,averageBB):
		height = swag.get_height()
		bb.text(swag.get_x()+swag.get_width()/2, height+2,value,ha="center",va="bottom")

	pdf.savefig()	
	plt.close()


	#Figure 2 contains average temperature followed by humidity from sensors across all rooms
	fig2 = plt.figure()
	tp = fig2.add_subplot(2,1,1)
	x1 = tp.bar(roomNum, meanTemp, align = "center",color = "r")
	plt.xticks(roomNum,roomIndex)
	tp.set_xlabel('Room')
	tp.set_ylabel('Temperature (degrees Celsius)')
	plt.title('Average Temperature of Room')
	swag1 = tp.patches
	meanTemp = np.around(meanTemp,decimals = 1)
	for swag, value in zip(swag1,meanTemp):
		height = swag.get_height()
		tp.text(swag.get_x()+swag.get_width()/2, height - 3,value,ha="center",va="bottom")

	hm = fig2.add_subplot(2,1,2)
	x2 = hm.bar(roomNum, meanHum, align = "center", color = "b")
	plt.xticks(roomNum,roomIndex)
	hm.set_xlabel('Room')
	hm.set_ylabel("Humidty")
	plt.title("Average Humidity of Room")
	swag2 = hm.patches
	meanHum = np.around(meanHum,decimals=1)
	for swag, value in zip(swag2,meanHum):
		height = swag.get_height()
		hm.text(swag.get_x()+swag.get_width()/2, height+1,value,ha="center",va="bottom")	
	plt.tight_layout()

	pdf.savefig()
	plt.close()



