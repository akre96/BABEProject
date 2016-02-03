# This script is intended to analyze all the rooms which have data
import os
import argparse
import glob
import numpy as np
from scripts.tempHum import tempHum
from scripts.beam import beam
from scripts.sheetUse import sheetUse
import matplotlib.pyplot as plt


#Adding support for command line arguments
parser = argparse.ArgumentParser(description='Process Data from all rooms')
parser.add_argument('-log', '-l', action='store_const',const=1,help='Include analysis from manual log in sheet')
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
			meanTemp.append(tempData['mean'])
			meanHum.append(humData['mean'])

			perDay, averagePerDay, indexDay = beam(roomBB[0])
			roomDict[int(room)] = averagePerDay
			averageBB.append(averagePerDay)

			roomIndex.append(room)

		except IndexError:
			notWorking.append(room)
	else:
		noData.append(room)


responseSheet = os.getcwd() + '/data/other/responses.csv'
sheetRooms, sheetAverage = sheetUse(responseSheet)


notWorking.sort()
print "Average temperature: %.2f C" % np.mean(meanTemp)
print "Average usage per day: %.2f" % np.mean(averageBB)
print "Rooms without data past 11/1/2015: "+' '.join(str(x) for x in notWorking)

roomIndex = sorted(roomDict.keys())
averageBB = [roomDict[x] for x in roomIndex]

roomNum = list(xrange(len(averageBB)))
sheetRoomNum = list(xrange(len(sheetAverage)))

#Figure 1 contains the average uses per day from Beam break followed by the uses recorded on lactation room sign in sheet
if (args.log == 1):
	fig1 = plt.figure()
	bb = fig1.add_subplot(2,1,1)
	x1 = bb.bar(roomNum,averageBB, align = "center", color = "g")
	plt.title("Average Uses per Day by Beam Break")
	plt.xticks(roomNum,roomIndex)
	bb.set_ylabel('Uses')
	bb.set_xlabel('Room')

	su = fig1.add_subplot(2,1,2)
	x1 = su.bar(sheetRoomNum,sheetAverage, align = "center", color = "y")
	plt.title("Average Uses per Day by Sign-In Log")
	plt.xticks(sheetRoomNum,sheetRooms)
	su.set_ylabel('Uses')
	su.set_xlabel('Room')

	plt.tight_layout()
else:
	fig1 = plt.figure()
	bb = fig1.add_subplot(1,1,1)
	x1 = bb.bar(roomNum,averageBB, align = "center", color = "g")
	plt.title("Average Uses per Day by Beam Break")
	plt.xticks(roomNum,roomIndex)
	bb.set_ylabel('Uses')
	bb.set_xlabel('Room')	

#Figure 2 contains average temperature followed by humidity from sensors across all rooms
fig2 = plt.figure()
tp = fig2.add_subplot(2,1,1)
x1 = tp.bar(roomNum, meanTemp, align = "center",color = "r")
plt.xticks(roomNum,roomIndex)
tp.set_xlabel('Room')
tp.set_ylabel('Temperature (degrees Celsius)')
plt.title('Average Temperature of Room')

hm = fig2.add_subplot(2,1,2)
x2 = hm.bar(roomNum, meanHum, align = "center", color = "b")
plt.xticks(roomNum,roomIndex)
hm.set_xlabel('Room')
hm.set_ylabel("Humidty")
plt.title("Average Humidity of Room")
plt.tight_layout()





plt.show()

