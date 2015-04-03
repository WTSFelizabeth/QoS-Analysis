#  pinganalysis.py
#  Created By:  Elizabeth Otto
#  Property Of: We Teach Science Foundation
#  Date Created:  10.13.14
#  Last Modified: 11.18.14
#  Description:  

import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
import csv
import datetime as dt

from dictionaries import months, numtodays, classtoday, locationtostart, locationtoend, blackboxlocationlist, classtoschool, blackboxschoollist
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

	#  Determine the date.
	year = 2015
	
	daysplit = filename.split('/')
	daysplit2 = daysplit[8]
	daysplit2 = daysplit2.split('.')
	daystr = daysplit2[0]
	day = int(daystr)

	monthstr = daysplit[7]
	month = months[monthstr]

	print month

	#  Find the day of the week.
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

def datetimecombine(date,times):

	datetimelist = list()

	for item in times:
		datetimeobject = dt.datetime(date.year,date.month,date.day,item.hour,item.minute,item.second)
		datetimelist.append(datetimeobject)

	return datetimelist

def graphdates(datalist,indexlist,school,startdate,enddate,smoothing=False):

	count = 0
	index = 0
	datetimelist = list()
	pinglist = list()
	jitterlist = list()
	losslist = list()

	for item in datalist:
		target = indexlist[index]
		if (count == target):
			datetimes = datetimecombine(item.date,item.times)
			datetimelist.extend(datetimes)
			pinglist.extend(item.pingtimes)
			jitterlist.extend(item.jitters)
			losslist.extend(item.losses)
			count += 1
			index += 1
		else:
			count += 1

	fig = plt.figure()

	plt.subplot(311)
	plt.plot(datetimelist,pinglist)
	plt.xlabel('Date')
	plt.ylabel('Ping Time (ms)')
	plt.axis([startdate,enddate,0,100])
	plt.gca().xaxis.set_major_formatter(mpl.dates.DateFormatter("%b %d"))

	plt.subplot(312)
	plt.plot(datetimelist,jitterlist)
	plt.xlabel('Date')
	plt.ylabel('Jitter (ms)')
	plt.axis([startdate,enddate,0,100])
	plt.gca().xaxis.set_major_formatter(mpl.dates.DateFormatter("%b %d"))

	plt.subplot(313)
	plt.plot(datetimelist,losslist)
	plt.xlabel('Date')
	plt.ylabel('% of packets lost')
	plt.axis([startdate,enddate,0,20])
	plt.gca().xaxis.set_major_formatter(mpl.dates.DateFormatter("%b %d"))

	fig.set_size_inches(10.5,18.5)

	fig.savefig(school+'_blackboxsummary')
	fig.clf()

	plt.close()

	return

#  Map times to reference time lists (due to skips in blackbox files).  Use previous data to fill in gaps.
def findtimes(reftimes,daytimes,daypings,dayjitters,daylosses):

	print 'test'

	return


#  Stack days of the week to create an 'average week' graph and metrics.
def stackdays(datalist,indexlist,startdate,enddate,includesessionday=True):

	count = 0
	index = 0
	datetimelist = list()
	pinglist = list()
	jitterlist = list()
	losslist = list()

	#  Establish reftimes list.
	i = 0
	reftimes = list()
	initialtime = dt.datetime(2015,1,1,0,0,0)
	timestep = dt.timedelta(0,0,0,0,1,0)

	while i < 1440:
		refdatetime = initialtime + timestep*i
		reftimes.append(refdatetime.time())
		i += 1

	for item in datalist:
		target = indexlist[index]


		if (count == target):
			
			if item.date >= startdate and item.date <= enddate:

				dayofweek = item.dayofweek
				daytimes = item.times
				daypings = item.pingtimes
				dayjitters = item.jitters
				daylosses = item.losses

				findtimes(reftimes,daytimes,daypings,dayjitters,daylosses)

				count += 1
				index += 1

		else:
			count += 1
		

	return

def sortblackboxdata(datalist):

	schoollist = list()
	
	for item in datalist:
		locations = item.location
		school = classtoschool[locations[0]]
		schoollist.append(school)


	for school in blackboxschoollist:

		index = 0
		indexlist = list()

		for item in datalist:
			if schoollist[index] == school:
				indexlist.append(index)
			index += 1

		if (indexlist != []):
			graphdates(datalist,indexlist,school,dt.datetime(2015,3,18),dt.datetime(2015,3,24))
			stackdays(datalist,indexlist,dt.date(2015,3,18),dt.date(2015,3,24))

	return

def pullsessiondata(data,location):

	starttime = locationtostart[location]
	endtime = locationtoend[location]

	length = len(data.times)
	i = 0

	timecut = list()
	pingcut = list()
	jittercut = list()
	losscut = list()

	while (i < length):
		if (data.times[i] >= starttime and data.times[i] <= endtime):
			timecut.append(data.times[i])
			pingcut.append(data.pingtimes[i])
			jittercut.append(data.jitters[i])
			losscut.append(data.losses[i])
			i += 1
		else:
			i += 1

	sessionData = BlackboxData(data.location,data.date,data.dayofweek,timecut,pingcut,jittercut,losscut,data.session)

	return sessionData

def blackboxanalyze(datalist):

	sessiondatalist = list()

	#  Loop over the full list of data.
	for item in datalist:
		#  If the data include a session, push to pullsessiondata to pull out a session data list.
		count = 0
		for flag in item.session:
			if flag == True:
				location = item.location[0]
				test = pullsessiondata(item,location)
				sessiondatalist.append(test)
		count += 1

	#  Plot data for each site.
	sortblackboxdata(datalist)

	return sessiondatalist