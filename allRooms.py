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
meanHum=[]
averageBB = []
notWorking = []
roomIndex=[]
noData=[]

#iterate through each room

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
			averageBB.append(averagePerDay)

			roomIndex.append(room)

		except IndexError:
			notWorking.append(room)
	else:
		noData.append(room)

notWorking.sort()
print "Average temperature: %.2f C" % np.mean(meanTemp)
print "Average usage per day: %.2f" % np.mean(averageBB)
print "Rooms without data past 11/1/2015: "+' '.join(str(x) for x in notWorking)



roomNum = list(xrange(len(averageBB)))
fig, ax = plt.subplots()
x1 = ax.bar(roomNum,averageBB, align = "center", color = "g")
plt.title("Average Uses per Day")
plt.xticks(roomNum,roomIndex)
ax.set_ylabel('Uses')
ax.set_xlabel('Room')

fig = plt.figure()
tp = fig.add_subplot(2,1,1)
x1 = tp.bar(roomNum, meanTemp, align = "center",color = "r")
plt.xticks(roomNum,roomIndex)
tp.set_xlabel('Room')
tp.set_ylabel('Temperature (degrees Celsius)')
plt.title('Average Temperature of Room')

hm = fig.add_subplot(2,1,2)
x2 = hm.bar(roomNum, meanHum, align = "center", color = "b")
plt.xticks(roomNum,roomIndex)
hm.set_xlabel('Room')
hm.set_ylabel("Humidty")
plt.title("Average Humidity of Room")
plt.tight_layout()





plt.show()

