# This script is intended to analyze all the rooms which have data
import os
import glob
import numpy as np
from scripts.tempHum import tempHum

#establish path to file in order to analyze data
currentDir = os.getcwd() +'/data/room'
meanTemp=[]
#iterate through each room
for subdir, dirs, files in os.walk(currentDir):
    for room in dirs:
    	currentRoom = currentDir+"/"+room
    	#Check if data in the rooms folder
        if os.listdir(currentRoom):
        	roomBB = glob.glob(currentRoom+'/BB*')
        	roomTH = glob.glob(currentRoom+'/TH*')

        	thDates, tempData, humData = tempHum(roomTH[0])
        	meanTemp.append(tempData['mean'])

print np.mean(meanTemp)

