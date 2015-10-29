from sys import argv
import glob
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import csv
from matplotlib.dates import date2num,num2date
from scripts.tempHum import tempHum
from scripts.beam import beam
from scripts.roomSummary import roomSummary

#Finding room to analyze and formatting it as file paths
room = raw_input('Which room number would you like to analyze? \n>>')
roomBB = glob.glob("data/room/"+room+"/BB*")
roomTH = glob.glob("data/room/"+room+"/TH*")

## BEAM BREAK

date, perDay, averagePerDay = beam(roomBB[0])

## TEMPERATURE AND HUMIDITY

date2, tempData, humData = tempHum(roomTH[0])



## ROOM SUMMARY
roomSummary(tempData,humData,averagePerDay)




##PLOTTING GRAPHS

#plotting beambreak frequency
fig, ax = plt.subplots()

bar_width = .7
y = {z:date.count(z) for z in date} #counting occurances/date
index = np.arange(len(y))
BB = plt.bar(index, y.values(), bar_width)

plt.xticks(index+bar_width/2,y.keys(), rotation=15)
plt.title('Beam Break Frequency')
ax.set_xlabel('Date')
ax.set_ylabel('Frequency (Breaks/Day)')

#plotting temperature and humidity
fig = plt.figure()
tp = fig.add_subplot(2,1,1)
x1 = tp.plot_date(date2,tempData['list'], xdate=True, ydate=False,fmt = 'ro-')
plt.xticks(rotation=0)
plt.setp(x1,linewidth=3,markersize = 2)
tp.set_xlabel('Time (minutes)')
tp.set_ylabel('Temperature (degrees Celsius)')
plt.title('Temperature of Room')

hm = fig.add_subplot(2,1,2)
x2 = hm.plot_date(date2,humData['list'], xdate=True, ydate=False, fmt = 'bo-')
plt.xticks(rotation=0)
plt.setp(x2,linewidth=3,markersize = 2)
plt.title('Humidity of Room')
hm.set_xlabel('Time (minutes)')
hm.set_ylabel('Percent Humidity')
plt.tight_layout()

plt.show()



