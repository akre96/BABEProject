# Use this script in order to analyze a single room
import argparse
from sys import argv
import sys
import glob
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import csv
from matplotlib.dates import date2num,num2date
from matplotlib.backends.backend_pdf import PdfPages
from scripts.tempHum import tempHum
from scripts.beam import beam
from scripts.roomSummary import roomSummary


#Adding support for command line arguments
parser = argparse.ArgumentParser(description='Process Data from a single room')
parser.add_argument('room', type=str, help='A room number to analyze')
parser.add_argument('-day','-d', action='store_const',const=1, help='Stops filtering beambreak data from 8am-10pm')
parser.add_argument('-week','-w', action='store_const',const=1, help='Stops filtering beambreak data for only weekdays')
args = parser.parse_args()

#Finding room to analyze and formatting it as file paths
room =  args.room
roomBB = glob.glob("data/room/"+room+"/BB*")
roomTH = glob.glob("data/room/"+room+"/TH*")


## BEAM BREAK
day = True
week = True
if args.day == 1:
	day = False
if args.week == 1:
	week = False

perDay, averagePerDay, indexDay = beam(roomBB[0],dayTime = day, weekDay = week)
		

## TEMPERATURE AND HUMIDITY

thDate, tempData, humData = tempHum(roomTH[0])



## ROOM SUMMARY
with open('graphs/room/'+str(args.room)+'_summary.txt', 'w+') as f:
    sys.stdout = f
    roomSummary(tempData,humData,averagePerDay,thDate)
file.closed
sys.stdout = sys.__stdout__

##PLOTTING GRAPHS
graphLoc = "graphs/room/"+str(args.room)+".pdf"


with PdfPages(graphLoc) as pdf:
	#plotting beambreak frequency
	fig = plt.figure()
	BB = fig.add_subplot(1,1,1)
	x = plt.plot_date([item[0] for item in perDay], [item[1] for item in perDay],xdate=True,ydate=False,fmt='go-')
	plt.xticks(rotation=10)

	plt.setp(x,linewidth=3,markersize = 2)
	plt.title('Beam Break Frequency')
	BB.set_xlabel('Date')
	BB.set_ylabel('Frequency (Breaks/Day)')
	pdf.savefig()	
	plt.close()

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

	pdf.savefig()	
	plt.close()





