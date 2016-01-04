# This script is intended to analyze all the rooms which have data
import os
import glob
import numpy as np
from scripts.tempHum import tempHum
from scripts.beam import beam
import matplotlib.pyplot as plt

#establish path to file in order to analyze data
currentDir = os.getcwd() +'/data/room'
meanTemp=[]
averageBB = []
notWorking = []
roomIndex=[]
noData=[]
#iterate through each room
for subdir, dirs, files in os.walk(currentDir):
    for room in dirs:
    	currentRoom = currentDir+"/"+room
    	#Check if data in the rooms folder
    	if os.listdir(currentRoom):
        	#Checks to see if any exceptions raised because no TH data in and ahead of 11/2015
        	try:
	        	roomBB = glob.glob(currentRoom+'/BB*')
	        	roomTH = glob.glob(currentRoom+'/TH*')

	        	thDates, tempData, humData = tempHum(roomTH[0])
	        	meanTemp.append(tempData['mean'])

	        	perHour, perDay, averagePerDay, indexHour, indexDay = beam(roomBB[0])
	        	averageBB.append(averagePerDay)
	        	roomIndex.append(room)
	        except IndexError:
	        	notWorking.append(room)
		else:
			noData.append(room)

notWorking.sort()
print "Average temperature: %.2f F" % np.mean(meanTemp)
print "Average usage per day: %.2f" % np.mean(averageBB)
print "Rooms without data past 11/1/2015: "+' '.join(str(x) for x in notWorking)



roomNum = list(xrange(len(averageBB)))
fig, ax = plt.subplots()
x1 = ax.bar(roomNum,averageBB, align = "center")
plt.xticks(roomNum,roomIndex)
ax.set_ylabel('Uses')
ax.set_xlabel('Room')
plt.show()

