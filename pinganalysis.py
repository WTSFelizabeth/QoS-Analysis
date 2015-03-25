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

from dictionaries import months, numtodays, classtoday, locationtostart, locationtoend
from pingdata import PingData, BlackboxData



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
def timefind(datetimestr,typeflag=True):

	#  Ping data format
	if typeflag == True:
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

	#  Blackbox data format
	if typeflag == False:
		#  Split the hour and minute
		timesplit = datetimestr.split(':')

		#  Find the hour, minute, and second.
		hour = int(timesplit[0])
		minute = int(timesplit[1])
		second = int(0)

		#  Create a time object.
		time = dt.time(hour,minute,second)

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
		date, location, bandwidth, times, pingtimes, jitters = pingread(filename)

		#  Create a PingData object, add to the list.
		data = PingData(location, date, bandwidth, times, pingtimes, jitters)

		pingdatalist.append(data)

	#  Return the list of PingData objects to main.py
	return pingdatalist


def blackboxread(file):

	filename = file

	#  initialize necessary lists and variables
	count = 0
	times = list()
	pingtimes = list()
	jitters = list()
	losses = list()
	session = list()

	#  Determine the date ### Will need to be changed for non-test data ###
	year = 2015
	monthstr = 'Mar'
	month = months[monthstr]
	daysplit = filename.split('/')
	daysplit = daysplit[7]
	daysplit = daysplit.split('.')
	daystr = daysplit[0]
	day = int(daystr)
	date = dt.date(year,month,day)
	dayofweekint = date.weekday()
	dayofweek = numtodays[dayofweekint]

	#  Determine the location(s) ### Will need to be changed for non-test data ###
	location = list()
	location.append('Testing')

	#  open the ping data file
	with open(filename, 'rb') as csvfile:
		filereader = csv.reader(csvfile)

		#  loop over the lines of the ping data file, add data 
		for line in filereader:
			if (count == 0):
				#  Increment count.
				count += 1
			
			#  Read each line into the relevant lists.	
			else:

				#  Parse the row to pull out the date/time stamp
				timestr = line[0]
				time = timefind(timestr,typeflag = False)
				times.append(time)

				#  Parse the row to pull out the ping time
				pingstr = line[1]
				ping = float(pingstr)
				pingtimes.append(ping)

				#  Parse the row to pull out the jitter
				jitterstr = line[2]
				jitter = float(jitterstr)
				jitters.append(jitter)

				#  Parse the row to pull out packet loss
				lossstr = line[3]
				loss = float(lossstr)
				losses.append(loss)

				count += 1

	#  Determine whether this dataset represents a session day (recursively for each location inclueded in file).
	count = 0
	for item in location:
		sessionday = classtoday[item]
		if (sessionday == dayofweek):
			session.append(True)
		else:
			session.append(False)
		count += 1

	#  Return all the relevant values.
	return date, dayofweek, location, times, pingtimes, jitters, losses, session

def blackboximport(filelist):

	blackboxdatalist = list()

	#  Read data in for each file in the list.
	for entry in filelist:

		#  Call blackbox read to read in the blackbox file.
		date, dayofweek, location, times, pingtimes, jitters, losses, session = blackboxread(entry)

		#  Create a BlackboxData object, add to the list.
		data = BlackboxData(location,date,dayofweek,times,pingtimes,jitters,losses,session)

		blackboxdatalist.append(data)


	return blackboxdatalist

def pullsessiondata(data,location):

	starttime = locationtostart[location]
	endtime = locationtoend[location]

	print starttime
	print endtime

	test = 'test'

	return test

def blackboxanalyze(datalist):

	#  Loop over the full list of data.
	for item in datalist:
		#  If the data include a session, push to pullsessiondata to pull out a session data list.
		count = 0
		for flag in item.session:
			if flag == True:
				location = item.location[0]
				test = pullsessiondata(item,location)
		count += 1

	return