#  pinganalysis.py
#  Created By:  Elizabeth Otto
#  Property Of: We Teach Science Foundation
#  Date Created:  10.13.14
#  Last Modified: 11.18.14
#  Description:  

from __future__ import division 

import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
import csv
import re
import datetime as dt

from dictionaries import months, numtodays, classtoday, locationtostart, locationtoend, classtoschool
from blackboxdictionaries import *

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

	#  add the path to the file name
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

				bandwidthre = re.compile('bandwidth*')
				matches = bandwidthre.search(line[2])

				#  Deal with exceptions where Sierramont files have doubled bandwidth line
				if matches != None:
					count += 1

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
	session = False

	#  Determine the date.
	
	daysplit = filename.split('/')
	daysplit2 = daysplit[9]
	daysplit2 = daysplit2.split('.')
	daystr = daysplit2[0]
	day = int(daystr)

	monthstr = daysplit[8]
	month = months[monthstr]

	yearstr = daysplit[7]
	year = int(yearstr)

	#  Find the day of the week.
	date = dt.date(year,month,day)
	dayofweekint = date.weekday()
	dayofweek = numtodays[dayofweekint]

	#  Determine the location(s)
	location = blackboxlocationconvert[daysplit[6]]

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

	#  Establish reftimes list to correct for problems in skipped minutes.
	i = 0
	reftimes = list()
	initialtime = dt.datetime(2015,1,1,0,0,0)
	timestep = dt.timedelta(0,0,0,0,1,0)

	while i < 1440:
		refdatetime = initialtime + timestep*i
		reftimes.append(refdatetime.time())
		i += 1

	correctedpings, correctedjitters, correctedlosses = findtimes(reftimes,times,pingtimes,jitters,losses)

	#  Determine whether this dataset represents a session day (recursively for each location inclueded in file).
	count = 0

	for item in location: 
		sessionsoutlist = blackboxdaysnosession[item]
		sessionsaddedlist = blackboxdayssessions[item]

		sessionday = classtoday[item]
		if (sessionday == dayofweek):
			session = True
		else:
			session = False

		for day in sessionsoutlist:
			if date == day.date():
				session = False

		for day in sessionsaddedlist:
			if date == day.date():
				session = True
		count += 1

	#  Return all the relevant values.
	return date, dayofweek, location, reftimes, correctedpings, correctedjitters, correctedlosses, session

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

def graphdates(schoolitemlist,school,startdate,enddate,smoothing=False):

	count = 0
	index = 0
	datetimelist = list()
	pinglist = list()
	jitterlist = list()
	losslist = list()

	for item in schoolitemlist:
		datetimes = datetimecombine(item.date,item.times)
		datetimelist.extend(datetimes)
		pinglist.extend(item.pingtimes)
		jitterlist.extend(item.jitters)
		losslist.extend(item.losses)

	datetimelist, pinglist, jitterlist, losslist = (list(t) for t in zip(*sorted(zip(datetimelist, pinglist, jitterlist, losslist))))

	fig = plt.figure()

	plt.subplot(311)
	plt.plot(datetimelist,pinglist)
	plt.xlabel('Date')
	plt.ylabel('Ping Time (ms)')
	plt.axis([startdate,enddate,0,30])
	plt.gca().xaxis.set_major_formatter(mpl.dates.DateFormatter("%b %d"))

	plt.subplot(312)
	plt.plot(datetimelist,jitterlist)
	plt.xlabel('Date')
	plt.ylabel('Jitter (ms)')
	plt.axis([startdate,enddate,0,60])
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

	timelength = len(reftimes)
	daylength = len(daytimes)
	i = 0
	j = 0
	pings = list()
	jitters = list()
	losses = list()

	while i < timelength:

		if j >= daylength:
			pings.append(daypings[j-1])
			jitters.append(dayjitters[j-1])
			losses.append(daylosses[j-1])
			i += 1
		elif reftimes[i] == daytimes[j]:
			pings.append(daypings[j])
			jitters.append(dayjitters[j])
			losses.append(daylosses[j])
			i += 1
			j += 1
		else:
			pings.append(daypings[j-1])
			jitters.append(dayjitters[j-1])
			losses.append(daylosses[j-1])
			i += 1

	return pings,jitters,losses


def plotweekcomp(hours,stackedweekday,stackedweekend,school):
	
	fig = plt.figure()

	plt.subplot(311)
	plt.plot(hours,stackedweekend[0],color = 'orange')
	plt.plot(hours,stackedweekday[0],color = 'blue')
	weekday = mpl.patches.Patch(color = 'blue',label = 'Average Weekday')
	weekend = mpl.patches.Patch(color = 'orange',label = 'Average Weekend')
	plt.legend(handles=[weekday,weekend],prop={'size':10})
	plt.axis([0,24,0,15])
	plt.title('Average Ping Time on Weekdays vs. Weekends')
	plt.xlabel('Hour of Day')
	plt.ylabel('Average Ping Time (ms)')

	plt.subplot(312)
	plt.plot(hours,stackedweekend[1],color = 'orange')
	plt.plot(hours,stackedweekday[1],color = 'blue')
	weekday = mpl.patches.Patch(color = 'blue',label = 'Average Weekday')
	weekend = mpl.patches.Patch(color = 'orange',label = 'Average Weekend')
	plt.legend(handles=[weekday,weekend],prop={'size':10})
	plt.axis([0,24,0,20])
	plt.title('Average Jitter on Weekdays vs. Weekends')
	plt.xlabel('Hour of Day')
	plt.ylabel('Jitter (ms)')

	plt.subplot(313)
	plt.plot(hours,stackedweekend[2],color = 'orange')
	plt.plot(hours,stackedweekday[2],color = 'blue')
	weekday = mpl.patches.Patch(color = 'blue',label = 'Average Weekday')
	weekend = mpl.patches.Patch(color = 'orange',label = 'Average Weekend')
	plt.legend(handles=[weekday,weekend],prop={'size':10})
	plt.axis([0,24,0,8])
	plt.title('Average Packet Loss on Weekdays vs. Weekends')
	plt.xlabel('Hour of Day')
	plt.ylabel('Average Packet Loss (%)')

	plt.suptitle('Weekday vs. Weekend Network - '+school,fontsize=20)

	fig.set_size_inches(10.5,18.5)

	fig.savefig('WeekdayvsWeekend'+'_'+school)

	fig.clf()
	plt.close()

	return

def plotsessioncomp(hours,stackedsession,stackedweek,school):

	fig = plt.figure()

	plt.subplot(311)
	plt.plot(hours,stackedweek[0],color = 'orange')
	plt.plot(hours,stackedsession[0],color = 'blue')
	session = mpl.patches.Patch(color = 'blue',label = 'Average Session Day')
	nosession = mpl.patches.Patch(color = 'orange',label = 'Average Non-Session Day')
	plt.legend(handles=[session,nosession],prop={'size':10})
	plt.axis([0,24,0,50])
	plt.title('Average Ping Time on Session vs. Non-Session Days')
	plt.xlabel('Hour of Day')
	plt.ylabel('Average Ping Time (ms)')

	plt.subplot(312)
	plt.plot(hours,stackedweek[1],color = 'orange')
	plt.plot(hours,stackedsession[1],color = 'blue')
	session = mpl.patches.Patch(color = 'blue',label = 'Average Session Day')
	nosession = mpl.patches.Patch(color = 'orange',label = 'Average Non-Session Day')
	plt.legend(handles=[session,nosession],prop={'size':10})
	plt.axis([0,24,0,50])
	plt.title('Average Jitter on Session vs. Non-Session Days')
	plt.xlabel('Hour of Day')
	plt.ylabel('Jitter (ms)')

	plt.subplot(313)
	plt.plot(hours,stackedweek[2],color = 'orange')
	plt.plot(hours,stackedsession[2],color = 'blue')
	session = mpl.patches.Patch(color = 'blue',label = 'Average Session Day')
	nosession = mpl.patches.Patch(color = 'orange',label = 'Average Non-Session Day')
	plt.legend(handles=[session,nosession],prop={'size':10})
	plt.axis([0,24,0,15])
	plt.title('Average Packet Loss on Session vs. Non-Session Days')
	plt.xlabel('Hour of Day')
	plt.ylabel('Average Packet Loss (%)')

	plt.suptitle('Session vs. Non-Session Weekday Network - '+school,fontsize=20)

	fig.set_size_inches(10.5,18.5)

	fig.savefig('SessionvsNoSession'+'_'+school)

	fig.clf()
	plt.close()

	return


#  Stack days of the week to create an 'average week' graph and metrics.
def stackdays(datalist,sessiondatalist,school,startdate,enddate):

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

	#  Declare np.array objects for each day of the week.
	monday = np.zeros((3,1440))
	tuesday = np.zeros((3,1440))
	wednesday = np.zeros((3,1440))
	thursday = np.zeros((3,1440))
	friday = np.zeros((3,1440))
	saturday = np.zeros((3,1440))
	sunday = np.zeros((3,1440))

	#  Declare np.array objects average standard deviations for each day of the week.
	monstandarddevs = np.zeros((3))
	tuestandarddevs = np.zeros((3))
	wedstandarddevs = np.zeros((3))
	thustandarddevs = np.zeros((3))
	fristandarddevs = np.zeros((3))
	satstandarddevs = np.zeros((3))
	sunstandarddevs = np.zeros((3))

	pingstack = np.zeros((100,1440))
	jitterstack = np.zeros((100,1440))
	lossstack = np.zeros((100,1440))

	#  Declare counts for each day of the week.
	moncount = 0
	tuecount = 0
	wedcount = 0
	thucount = 0
	fricount = 0
	satcount = 0
	suncount = 0

	count = 0


	for item in datalist:

		excludedlist = blackboxdaysout[school]
		excluded = False

		for excludeddate in excludedlist:
			if item.date == excludeddate.date():
				excluded = True
			
		if item.date >= startdate.date() and item.date <= enddate.date() and excluded == False:

			dayofweek = item.dayofweek
			daytimes = item.times
			daypings = item.pingtimes
			dayjitters = item.jitters
			daylosses = item.losses

				#  Stack corrected values to the correct day of the week.
			if dayofweek == 'Mon':
				monday[0] += np.array(daypings)
				pingstack[count] = np.array(daypings)
				monday[1] += np.array(dayjitters)
				jitterstack[count] = np.array(dayjitters)
				monday[2] += np.array(daylosses)
				lossstack = np.array(daylosses)
				monstandarddevs[0] += np.std(monday[0])
				monstandarddevs[1] += np.std(monday[1])
				monstandarddevs[2] += np.std(monday[2])
				moncount += 1
			elif dayofweek == 'Tue':
				tuesday[0] += np.array(daypings)
				pingstack[count] = np.array(daypings)
				tuesday[1] += np.array(dayjitters)
				jitterstack[count] = np.array(dayjitters)
				tuesday[2] += np.array(daylosses)
				lossstack = np.array(daylosses)
				tuestandarddevs[0] += np.std(tuesday[0])
				tuestandarddevs[1] += np.std(tuesday[1])
				tuestandarddevs[2] += np.std(tuesday[2])
				tuecount += 1
			elif dayofweek == 'Wed':
				wednesday[0] += np.array(daypings)
				pingstack[count] = np.array(daypings)
				wednesday[1] += np.array(dayjitters)
				jitterstack[count] = np.array(dayjitters)
				wednesday[2] += np.array(daylosses)
				lossstack = np.array(daylosses)
				wedstandarddevs[0] += np.std(wednesday[0])
				wedstandarddevs[1] += np.std(wednesday[1])
				wedstandarddevs[2] += np.std(wednesday[2])
				wedcount += 1
			elif dayofweek == 'Thu':
				thursday[0] += np.array(daypings)
				pingstack[count] = np.array(daypings)
				thursday[1] += np.array(dayjitters)
				jitterstack[count] = np.array(dayjitters)
				thursday[2] += np.array(daylosses)
				lossstack = np.array(daylosses)
				thustandarddevs[0] += np.std(thursday[0])
				thustandarddevs[1] += np.std(thursday[1])
				thustandarddevs[2] += np.std(thursday[2])
				thucount += 1
			elif dayofweek == 'Fri':
				friday[0] += np.array(daypings)
				pingstack[count] = np.array(daypings)
				friday[1] += np.array(dayjitters)
				jitterstack[count] = np.array(dayjitters)
				friday[2] += np.array(daylosses)
				lossstack = np.array(daylosses)
				fristandarddevs[0] += np.std(friday[0])
				fristandarddevs[1] += np.std(friday[1])
				fristandarddevs[2] += np.std(friday[2])
				fricount += 1
			elif dayofweek == 'Sat':
				saturday[0] += np.array(daypings)
				pingstack[count] = np.array(daypings)
				saturday[1] += np.array(dayjitters)
				jitterstack[count] = np.array(dayjitters)
				saturday[2] += np.array(daylosses)
				lossstack = np.array(daylosses)
				satstandarddevs[0] += np.std(saturday[0])
				satstandarddevs[1] += np.std(saturday[1])
				satstandarddevs[2] += np.std(saturday[2])
				satcount += 1
			elif dayofweek == 'Sun':
				sunday[0] += np.array(daypings)
				pingstack[count] = np.array(daypings)
				sunday[1] += np.array(dayjitters)
				jitterstack[count] = np.array(dayjitters)
				sunday[2] += np.array(daylosses)
				lossstack = np.array(daylosses)
				sunstandarddevs[0] += np.std(sunday[0])
				sunstandarddevs[1] += np.std(sunday[1])
				sunstandarddevs[2] += np.std(sunday[2])
				suncount += 1

			count += 1

	#  Calculate averages for each day of the week.
	monaverage = monday/moncount
	tueaverage = tuesday/tuecount
	wedaverage = wednesday/wedcount
	thuaverage = thursday/thucount
	friaverage = friday/fricount
	sataverage = saturday/satcount
	sunaverage = sunday/suncount


	#  Calculate averages standard deviations for each day of the week.
	monstandarddevs = monstandarddevs/moncount
	tuestandarddevs = tuestandarddevs/tuecount
	wedstandarddevs = wedstandarddevs/wedcount
	thustandarddevs = thustandarddevs/thucount
	fristandarddevs = fristandarddevs/fricount
	satstandarddevs = satstandarddevs/satcount
	sunstandarddevs = sunstandarddevs/suncount

	#  Stack weekends and weekdays for this school site, then plot stacked results.
	stackedweekday = np.array((3,1440))
	stackedweekend = np.array((3,1440))
	stackedweekdaystd = np.array((3))
	stackedweekendstd = np.array((3))

	stackedweekday = (monaverage+tueaverage+wedaverage+thuaverage+friaverage)/5
	stackedweekdaystd = (monstandarddevs+tuestandarddevs+wedstandarddevs+thustandarddevs+fristandarddevs)/5
	stackedweekend = (sataverage+sunaverage)/2
	stackedweekendstd = (satstandarddevs+sunstandarddevs)/2
	hours = np.linspace(0,24,num=1440)

	plotweekcomp(hours,stackedweekday,stackedweekend,school)

	#  Pull out and compare non-session days to session days.  
	sessiondaystr = blackboxschooltoday[school]

	#  Find average session and non-session days.
	if sessiondaystr == 'Mon':
		sessionaverage = monaverage
		sesssionstd = monstandarddevs
		nosessionaverage = (tueaverage+wedaverage+thuaverage+friaverage)/4
	elif sessiondaystr == 'Tue':
		sessionaverage = tueaverage
		sessionstd = tuestandarddevs
		nosessionaverage = (monaverage+wedaverage+thuaverage+friaverage)/4
		nosessionstd = (monstandarddevs+wedstandarddevs+thustandarddevs+fristandarddevs)/4
	elif sessiondaystr == 'Wed':
		sessionaverage = wedaverage
		sessionstd = wedstandarddevs
		nosessionaverage = (monaverage+tueaverage+thuaverage+friaverage)/4
	elif sessiondaystr == 'Thu':
		sessionaverage = thuaverage
		sessionstd = thustandarddevs
		nosessionaverage = (monaverage+tueaverage+wedaverage+friaverage)/4

	plotsessioncomp(hours,sessionaverage,nosessionaverage,school)

	#  Pull out and compare session times to the same times on other days.

	#  Declare necessary lists:
	loclist = list()
	numberofcompsessions = 0
	pingarray = np.zeros([4,100])	
	jitterarray = np.zeros([4,100])
	lossarray = np.zeros([4,100])


	for item in sessiondatalist:

		excludedlist = blackboxdaysout[school]
		excluded = False

		for excludeddate in excludedlist:
			if item.date == excludeddate.date():
				excluded = True


		if item.date >= startdate.date() and item.date <= enddate.date() and excluded == False:
			timelen = len(item.times)
			locations = item.location
			loclist.extend(locations)

			#  Find session data
			itempings = item.pingtimes
			itemjitters = item.jitters
			itemlosses = item.losses
			itemdayofweek = item.dayofweek

			#  Loop over each class session associated with this blackbox session
			for location in locations:
				starttime = locationtostart[location]
				endtime = locationtoend[location]

				i = 0
				sessionminutes = 0
				nosessiontimes = list()
				nosessionpings = list()
				nosessionjitters = list()
				nosessionlosses = list()

				#  Pull same times from nosessionaverage list
				while i < 1440:
					if (reftimes[i] >= starttime) and (reftimes[i] <= endtime):
						nosessiontimes.append(reftimes[i])
						nosessionpings.append(nosessionaverage[0,i])
						nosessionjitters.append(nosessionaverage[1,i])
						nosessionlosses.append(nosessionaverage[2,i])

					i += 1

				#  Begin calculation of reference standard deviations
				refpingstdevtot = 0
				refjitterstdevtot = 0
				reflossstdevtot = 0
				refcount = 0

				for fulldata in datalist:
					#  Get day of week
					fulldatadayofweek = fulldata.dayofweek

					excludedlist2 = blackboxdaysout[school]
					excluded2 = False

					for excludeddate2 in excludedlist2:
						if fulldata.date == excludeddate2.date():
							excluded2 = True

					#  Check to make sure this isn't a session day or a weekend.
					if (fulldatadayofweek != itemdayofweek) and (fulldatadayofweek != 'Sun') and (fulldatadayofweek != 'Sat') and excluded2 == False:
						
						fulldatatemppinglist = list()
						fulldatatempjitterlist = list()
						fulldatatemplosslist = list()

						#  Pull out analogous session times.
						i = 0
						while i < 1440:
							if (reftimes[i] >= starttime) and (reftimes[i] <= endtime):
								fulldatatemppinglist.append(fulldata.pingtimes[i])
								fulldatatempjitterlist.append(fulldata.jitters[i])
								fulldatatemplosslist.append(fulldata.losses[i])
							i += 1

						#  Calculate standard deviation over reference ping times.
						if fulldatatemppinglist != []:
							temppingstdev = np.std(np.array(fulldatatemppinglist))
							tempjitterstdev = np.std(np.array(fulldatatempjitterlist))
							templossstdev = np.std(np.array(fulldatatemplosslist))
							refpingstdevtot += temppingstdev
							refjitterstdevtot += tempjitterstdev
							reflossstdevtot += templossstdev
							refcount += 1

				#  Finish calculation of reference standard deviations.
				refpingstdev = refpingstdevtot/refcount
				refjitterstdev = refjitterstdevtot/refcount
				reflossstdev = reflossstdevtot/refcount

				#  Calculate statistics for ping times.
				itempingsaverage = np.mean(np.array(itempings))
				itempingsstd = np.std(np.array(itempings))
				nosessionpingsaverage = np.mean(np.array(nosessionpings))

				pingarray[0,numberofcompsessions] = itempingsaverage
				pingarray[1,numberofcompsessions] = itempingsstd
				pingarray[2,numberofcompsessions] = nosessionpingsaverage
				pingarray[3,numberofcompsessions] = refpingstdev

				#  Calculate statistics for jitter.
				itemjittersaverage = np.mean(np.array(itemjitters))
				itemjittersstd = np.std(np.array(itemjitters))
				nosessionjittersaverage = np.mean(np.array(nosessionjitters))

				jitterarray[0,numberofcompsessions] = itemjittersaverage
				jitterarray[1,numberofcompsessions] = itemjittersstd
				jitterarray[2,numberofcompsessions] = nosessionjittersaverage
				jitterarray[3,numberofcompsessions] = refjitterstdev

				#  Calculate statistics for packet loss.
				itemlossesaverage = np.mean(np.array(itemlosses))
				itemlossesstd = np.std(np.array(itemlosses))
				nosessionlossesaverage = np.mean(np.array(nosessionlosses))

				lossarray[0,numberofcompsessions] = itemlossesaverage
				lossarray[1,numberofcompsessions] = itemlossesstd
				lossarray[2,numberofcompsessions] = nosessionlossesaverage
				lossarray[3,numberofcompsessions] = reflossstdev

				numberofcompsessions += 1

	return loclist,numberofcompsessions,pingarray,jitterarray,lossarray


def sessionvsnostats(pingarray,jitterarray,lossarray,count):

	pings = pingarray[0,0:(count)]
	jitters = jitterarray[0,0:(count)]
	losses = lossarray[0,0:(count)]

	pingavg = np.sum(pings)/count
	jitteravg = np.sum(jitters)/count
	lossavg = np.sum(losses)/count

	pingcomps = pingarray[2,0:(count)]
	jittercomps = jitterarray[2,0:(count)]
	losscomps = lossarray[2,0:(count)]

	pingcompavg = np.sum(pingcomps)/count
	jittercompavg = np.sum(jittercomps)/count
	losscompavg = np.sum(losscomps)/count

	pingdel = pingavg-pingcompavg
	jitterdel = jitteravg-jittercompavg
	lossdel = lossavg-losscompavg

	pingstdevs = pingarray[1,0:(count)]
	jitterstdevs = jitterarray[1,0:(count)]
	lossstdevs = lossarray[1,0:(count)]

	pingsquares = np.sum(np.square(pingstdevs))
	jittersquares = np.sum(np.square(jitterstdevs))
	losssquares = np.sum(np.square(lossstdevs))

	pingstdev = np.sqrt(pingsquares/count)
	jitterstdev = np.sqrt(jittersquares/count)
	lossstdev = np.sqrt(losssquares/count)

	pingcompstdevs = pingarray[3,0:(count)]
	jittercompstdevs = jitterarray[3,0:(count)]
	losscompstdevs = lossarray[3,0:(count)]

	pingcompsquares = np.sum(np.square(pingcompstdevs))
	jittercompsquares = np.sum(np.square(jittercompstdevs))
	losscompsquares = np.sum(np.square(losscompstdevs))

	pingcompstdev = np.sqrt(pingcompsquares/count)
	jittercompstdev = np.sqrt(jittercompsquares/count)
	losscompstdev = np.sqrt(losscompsquares/count)

	pingstat = pingdel/pingcompstdev
	jitterstat = jitterdel/jittercompstdev
	lossstat = lossdel/losscompstdev

	return pingstat, jitterstat, lossstat

def stattoprob(pingstat,jitterstat,lossstat):

	ping1 = sp.stats.norm.cdf(np.abs(pingstat))
	ping2 = sp.stats.norm.cdf(-1*np.abs(pingstat))
	pingprob = ping1-ping2

	jitter1 = sp.stats.norm.cdf(np.abs(jitterstat))
	jitter2 = sp.stats.norm.cdf(-1*np.abs(jitterstat))
	jitterprob = jitter1-jitter2

	loss1 = sp.stats.norm.cdf(np.abs(lossstat))
	loss2 = sp.stats.norm.cdf(-1*np.abs(lossstat))
	lossprob = loss1-loss2

	return pingprob, jitterprob, lossprob

def sortblackboxdata(datalist,sessiondatalist):

	schooldatalist = list()

	for school in blackboxschoollist:

		schoolitemlist = list()
		sessionslist = list()

		for item in datalist:
			locations = item.location
			itemschool = classtoschool[locations[0]]
			startdategraph = (blackboxstartandendforgraph[itemschool])[0]
			enddategraph = (blackboxstartandendforgraph[itemschool])[1]
			startdateanalysis = (blackboxstartandendforanalysis[itemschool])[0]
			enddateanalysis = (blackboxstartandendforanalysis[itemschool])[1]
			if itemschool == school:
				schoolitemlist.append(item)

		for item in sessiondatalist:
			itemschool = classtoschool[item.location[0]]
			if itemschool == school:
				sessionslist.append(item)


		if (schoolitemlist != []):
			graphdates(schoolitemlist,school,startdategraph,enddategraph)
			loclist,count,pingarray,jitterarray,lossarray = stackdays(schoolitemlist,sessionslist,school,startdateanalysis,enddateanalysis)

			#  Plot comparisons between session and no session.
			fig = plt.figure()

			#  Compare ping time
			plt.subplot(311)
			ind = np.linspace(1,count,num=count)
			ind2 = np.linspace(1.2,count+0.2,num=count)
			plotarray = pingarray[0,0:(count)]
			plotarray = plotarray.transpose()
			ploterrors = pingarray[1,0:(count)]
			ploterrors = ploterrors.transpose()
			comparray = pingarray[2,0:(count)]
			comparray = comparray.transpose()
			comperrors = pingarray[3,0:(count)]
			comperrors = comperrors.transpose()
			minimum = np.min(plotarray) - 2
			maximum = np.max(plotarray) + 2
			plt.plot(ind,plotarray,'bo',ind2,comparray,'ro')
			plt.errorbar(ind,plotarray,yerr=ploterrors,fmt='o')
			plt.errorbar(ind2,comparray,yerr=comperrors,fmt='o')
			plt.axis([0,count+2,minimum,maximum])
			plt.xlabel('Session Number')
			plt.ylabel('Average Ping Time (ms)')
			plt.title('Session vs. No Session - Ping Time')
			blue = mpl.patches.Patch(color = 'blue', label = 'Session Average')
			green = mpl.patches.Patch(color = 'green', label = 'Comparison Average')
			plt.legend(handles=[blue,green],prop={'size':12})

			#  Compare jitter
			plt.subplot(312)
			plotarray = jitterarray[0,0:(count)]
			plotarray = plotarray.transpose()
			ploterrors = jitterarray[1,0:(count)]
			ploterrors = ploterrors.transpose()
			comparray = jitterarray[2,0:(count)]
			comparray = comparray.transpose()
			comperrors = jitterarray[3,0:(count)]
			comperrors = comperrors.transpose()
			minimum = np.min(plotarray) - 2
			maximum = np.max(plotarray) + 2
			plt.plot(ind,plotarray,'bo',ind2,comparray,'ro')
			plt.errorbar(ind,plotarray,yerr=ploterrors,fmt='o')
			plt.errorbar(ind2,comparray,yerr=comperrors,fmt='o')
			plt.axis([0,count+2,minimum,maximum])
			plt.xlabel('Session Number')
			plt.ylabel('Jitter (ms)')
			plt.title('Session vs. No Session - Jitter')

			#  Compare % loss
			plt.subplot(313)
			plotarray = lossarray[0,0:(count)]
			plotarray = plotarray.transpose()
			ploterrors = lossarray[1,0:(count)]
			ploterrors = ploterrors.transpose()
			comparray = lossarray[2,0:(count)]
			comparray = comparray.transpose()
			comperrors = lossarray[3,0:(count)]
			comperrors = comperrors.transpose()
			minimum = np.min(plotarray) - 2
			maximum = np.max(plotarray) + 2
			plt.plot(ind,plotarray,'bo',ind2,comparray,'ro')
			plt.errorbar(ind,plotarray,yerr=ploterrors,fmt='o')
			plt.errorbar(ind2,comparray,yerr=comperrors,fmt='o')
			plt.axis([0,count+2,minimum,maximum])
			plt.xlabel('Session Number')
			plt.ylabel('Percent Packet Loss')
			plt.title('Session vs. No Session - Percent Packet Loss')

			plt.suptitle('Session vs. No Session Comparison - '+school, fontsize=20)

			fig.set_size_inches(10.5,18.5)

			fig.savefig('SessionComp'+'_'+school)

			plt.close()

			fig.clf()

			pingstat, jitterstat, lossstat = sessionvsnostats(pingarray,jitterarray,lossarray,count)
			pingprob, jitterprob, lossprob = stattoprob(pingstat,jitterstat,lossstat)

			print 'At',school,', the session pings are',pingstat,'standard devations away from the mean on non-session days at the same time.'
			print 'Probability of statistical significance =',pingprob,'(based on',count,'sessions)'

			print 'At',school,', the session jitter is',jitterstat,'standard devations away from the mean on non-session days at the same time.'
			print 'Probability of statistical significance =',jitterprob,'(based on',count,'sessions)'

			print 'At',school,', the session packet loss is',lossstat,'standard devations away from the mean on non-session days at the same time.'
			print 'Probability of statistical significance =',lossprob,'(based on',count,'sessions)'

	return

def pullsessiondata(data,location):

	starttime = locationtostart[location]
	endtime = locationtoend[location]

	dayofweek = data.dayofweek
	date = data.date

	extrasessions = blackboxdayssessions[location]

	for item in extrasessions:
		if date == item:
			starttime = blackboxspecialtimesstart[location]
			endtime = blackboxspecialtimesend[location]

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

	loclist = list()
	loclist.append(location)

	sessionData = BlackboxData(loclist,data.date,data.dayofweek,timecut,pingcut,jittercut,losscut,data.session)

	return sessionData

def blackboxanalyze(datalist):

	sessiondatalist = list()

	#  Loop over the full list of data.
	for item in datalist:
		#  If the data include a session, push to pullsessiondata to pull out a session data list.
		if item.session == True:
			for location in item.location:
				test = pullsessiondata(item,location)
				sessiondatalist.append(test)

	#  Plot data for each site.
	sortblackboxdata(datalist,sessiondatalist)

	return sessiondatalist