#  pinganalysis.py
#  Created By:  Elizabeth Otto
#  Property Of: We Teach Science Foundation
#  Date Created:  10.13.14
#  Last Modified: 11.18.14
#  Description:  

import numpy as np
import scipy as sp
import matplotlib as mpl
import csv
import datetime as dt

from dictionaries import months
from pingdata import PingData



#  Checks for errors in a line of the incoming ping file.  Will be implemented later.
def errorchecks():

	return


#  Separates out the bandwidth from the first line of ping file.
def bandwidthfind(bandwidthstr):

	splitbandwidthstr1 = bandwidthstr.split()
	splitbandwidthstr2 = splitbandwidthstr1[1]
	splitbandwidthstr3 = splitbandwidthstr2.split('k')
	bandwidthstr = splitbandwidthstr3[0]
	
	#  Record the bandwidth as an integer.
	bandwidth = int(bandwidthstr)

	#  Return the bandwidth
	return bandwidth


#  Separates out the date from the time stamp and returns it as a date object (from the datetime module).
def datefind(datetimestr, format):
	
	#  Split the date fromt the time stamp.  Format 1 = ping format, Format 2 = survey format
	if format == 1:
		datesplit = datetimestr.split()
		datesplit = datesplit[0]
	if format == 2:
		datesplit = datetimestr.split('_')
		datesplit = datesplit[0]

	#  Split the day, month, and year from the datestamp.
	datesplit = datesplit.split('-')

	#  Find the day, month, and year.
	day = int(datesplit[0])
	month = months[datesplit[1]]
	year = int(datesplit[2])

	#  Create a date object.
	date = dt.date(year,month,day)

	#  Return the date.
	return date

#  Separates out the time from the time stamp and retursn it as a time object (from the datetime module).
def timefind(datetimestr):

	#  Split the time from the date stamp.
	datetimesplit = datetimestr.split()
	datesplit = datetimesplit[0]
	timesplit = datetimesplit[1]

	#  Split the date.
	datesplit = datesplit.split('-')

	#  Find the day, month, and year.
	day = int(datesplit[0])
	month = months[datesplit[1]]
	year = int(datesplit[2])

	#  Split the hour, minute, and second.
	timesplit = timesplit.split(':')

	#  Find the hour, minute, and second.
	hour = int(timesplit[0])
	minute = int(timesplit[1])
	second = int(timesplit[2])

	#  Create a time object.
	time = dt.datetime(year,month,day,hour, minute, second)

	#  Return the time.
	return time


#  Reads in the data from a single ping log, formats for creating the PingData object.
def pingread(file):

	#  add the path to the file name  ##CHANGE THIS###
	filename = file

	#  initialize necessary lists and variables
	count = 0
	bandwidth = 0.0
	location = ''
	times = list()
	pingtimes = list()
	jitters = list()

	#  open the ping data file
	with open(filename, 'rb') as csvfile:
		filereader = csv.reader(csvfile)

		#  loop over the lines of the ping data file, add data 
		for line in filereader:
			#  The first line of the file has the bandwidth instead of a ping time.
			#  Record it as well as the location and date , which only need to be set once per file.
			if (count == 0):
				
				#  Parse the top row to pull out the date.
				date = datefind(line[0],1)

				#  Parse the top row to pull out the location
				location = line[1]

				#  Parse the top row to pull out the bandwidth				
				bandwidth = bandwidthfind(line[2])

				#  Increment count.
				count += 1
			
			#  Read each line into the relevant lists.	
			else:

				#  Parse the row to pull out the date/time stamp
				timestr = line[0]
				time = timefind(timestr)
				times.append(time)

				#  Parse the row to pull out the ping time
				pingstr = line[2]
				ping = float(pingstr)
				pingtimes.append(ping)

				#  Parse the row to pull out the jitter
				jitterstr = line[3]
				jitter = float(jitterstr)
				jitters.append(jitter)

				count += 1

	#  Return all the relevant values.
	return date, location, bandwidth, times, pingtimes, jitters


#  Controller for importing all ping files.
def pingimport(filelist):

	pingdatalist = list()

	for entry in filelist:

		#  Call pingread to read in the ping file.
		filename = entry
		print filename
		date, location, bandwidth, times, pingtimes, jitters = pingread(filename)

		#  Create a PingData object, add to the list.
		data = PingData(location, date, bandwidth, times, pingtimes, jitters)

		pingdatalist.append(data)

	#  Return the list of PingData objects to main.py
	return pingdatalist