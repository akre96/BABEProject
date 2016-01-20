# Use this script in order to analyze a single room
import argparse
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


#Adding support for command line arguments
parser = argparse.ArgumentParser(description='Process Data from a single room')
parser.add_argument('room', type=str, help='A room number to analyze')
args = parser.parse_args()

#Finding room to analyze and formatting it as file paths
room =  args.room
roomBB = glob.glob("data/room/"+room+"/BB*")
roomTH = glob.glob("data/room/"+room+"/TH*")

## BEAM BREAK

perDay, averagePerDay, indexDay = beam(roomBB[0])

## TEMPERATURE AND HUMIDITY

thDate, tempData, humData = tempHum(roomTH[0])



## ROOM SUMMARY
roomSummary(tempData,humData,averagePerDay)


##PLOTTING GRAPHS

#plotting beambreak frequency
fig, ax = plt.subplots()

bar_width = .7

BB = plt.bar(indexDay, [item[1] for item in perDay], bar_width)

plt.xticks(indexDay,[item[0] for item in perDay], rotation=15)
plt.title('Beam Break Frequency')
ax.set_xlabel('Date')
ax.set_ylabel('Frequency (Breaks/Day)')

#plotting temperature and humidity
fig = plt.figure()
tp = fig.add_subplot(2,1,1)
x1 = tp.plot_date(thDate,tempData['list'], xdate=True, ydate=False,fmt = 'ro-')
plt.xticks(rotation=10)
plt.setp(x1,linewidth=3,markersize = 2)
tp.set_xlabel('Time (minutes)')
tp.set_ylabel('Temperature (degrees Celsius)')
plt.title('Temperature of Room')

hm = fig.add_subplot(2,1,2)
x2 = hm.plot_date(thDate,humData['list'], xdate=True, ydate=False, fmt = 'bo-')
plt.xticks(rotation=10)
plt.setp(x2,linewidth=3,markersize = 2)
plt.title('Humidity of Room')
hm.set_xlabel('Time (minutes)')
hm.set_ylabel('Percent Humidity')
plt.tight_layout()

plt.show()



