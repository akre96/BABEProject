##ROOM SUMMARY
#	Prints color formatted summary of a single rooms beam break 
#	and temp/humidity data to terminal.


def	roomSummary(tempData,humData,averagePerDay,date):

	class bcolors:
	    HEADER = '\033[95m'
	    OKBLUE = '\033[94m'
	    OKGREEN = '\033[92m'
	    WARNING = '\033[93m'
	    FAIL = '\033[91m'
	    ENDC = '\033[0m'
	    BOLD = '\033[1m'
	    UNDERLINE = '\033[4m'

	print bcolors.HEADER +'SUMMARY:' + bcolors.ENDC
	print ' '
	print 'Time below sixty: '+str(humData['belowSixty']/60)+' hours'
	print 'Time above ninety: '+str(humData['aboveNinety']/60)+' hours'
	print ' '

	print 'Temperature Ranged from: '+str(tempData['min'])+' to '+str(tempData['max'])+' Degrees Celsius'
	print 'Mean Temperature: '+str(tempData['mean'])+' Degrees Celsius'
	print 'Temperature Variance is: '+str(tempData['var'])+' Degrees Celsius'

	print ' '

	print 'Humidity Ranged from: '+str(humData['min'])+' to '+str(humData['max'])+' Percent Humidity'
	print 'Mean Humidity: '+str(humData['mean'])+' Percent Humidity'
	print 'Humidity Variance is: '+str(humData['var'])+' Percent Humidity'
	print ' '
	print 'Room uses per day: '+str(averagePerDay)+' Uses'
	print ' '
	print 'Last data entry: ' +date[-1].strftime('%b %d %Y')
	print ' '
	return