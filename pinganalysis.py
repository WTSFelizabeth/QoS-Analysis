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
import datetime as dt

from dictionaries import months, numtodays, classtoday, locationtostart, locationtoend, blackboxlocationlist, classtoschool, blackboxschoollist
from dictionaries import blackboxschooltoday
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
	plt.plot(hours,stackedweekday[1],color = 'blue')
	weekday = mpl.patches.Patch(color = 'blue',label = 'Average Weekday')
	weekend = mpl.patches.Patch(color = 'orange',label = 'Average Weekend')
	plt.legend(handles=[weekday,weekend],prop={'size':10})
	plt.axis([0,24,0,50])
	plt.title('Average Ping Time on Weekdays vs. Weekends')
	plt.xlabel('Hour of Day')
	plt.ylabel('Average Ping Time (ms)')

	plt.subplot(312)
	plt.plot(hours,stackedweekend[1],color = 'orange')
	plt.plot(hours,stackedweekday[1],color = 'blue')
	weekday = mpl.patches.Patch(color = 'blue',label = 'Average Weekday')
	weekend = mpl.patches.Patch(color = 'orange',label = 'Average Weekend')
	plt.legend(handles=[weekday,weekend],prop={'size':10})
	plt.axis([0,24,0,50])
	plt.title('Average Jitter on Weekdays vs. Weekends')
	plt.xlabel('Hour of Day')
	plt.ylabel('Jitter (ms)')

	plt.subplot(313)
	plt.plot(hours,stackedweekend[2],color = 'orange')
	plt.plot(hours,stackedweekday[2],color = 'blue')
	weekday = mpl.patches.Patch(color = 'blue',label = 'Average Weekday')
	weekend = mpl.patches.Patch(color = 'orange',label = 'Average Weekend')
	plt.legend(handles=[weekday,weekend],prop={'size':10})
	plt.axis([0,24,0,15])
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
	plt.plot(hours,stackedsession[1],color = 'blue')
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
			
		if item.date >= startdate and item.date <= enddate:

			dayofweek = item.dayofweek
			daytimes = item.times
			daypings = item.pingtimes
			dayjitters = item.jitters
			daylosses = item.losses

			#  Correct for skipped minutes
			correctedpings, correctedjitters, correctedlosses = findtimes(reftimes,daytimes,daypings,dayjitters,daylosses)

				#  Stack corrected values to the correct day of the week.
			if dayofweek == 'Mon':
				monday[0] += np.array(correctedpings)
				pingstack[count] = np.array(correctedpings)
				monday[1] += np.array(correctedjitters)
				jitterstack[count] = np.array(correctedjitters)
				monday[2] += np.array(correctedlosses)
				lossstack = np.array(correctedlosses)
				monstandarddevs[0] += np.std(monday[0])
				monstandarddevs[1] += np.std(monday[1])
				monstandarddevs[2] += np.std(monday[2])
				moncount += 1
			elif dayofweek == 'Tue':
				tuesday[0] += np.array(correctedpings)
				pingstack[count] = np.array(correctedpings)
				tuesday[1] += np.array(correctedjitters)
				jitterstack[count] = np.array(correctedjitters)
				tuesday[2] += np.array(correctedlosses)
				lossstack = np.array(correctedlosses)
				tuestandarddevs[0] += np.std(tuesday[0])
				tuestandarddevs[1] += np.std(tuesday[1])
				tuestandarddevs[2] += np.std(tuesday[2])
				tuecount += 1
			elif dayofweek == 'Wed':
				wednesday[0] += np.array(correctedpings)
				pingstack[count] = np.array(correctedpings)
				wednesday[1] += np.array(correctedjitters)
				jitterstack[count] = np.array(correctedjitters)
				wednesday[2] += np.array(correctedlosses)
				lossstack = np.array(correctedlosses)
				wedstandarddevs[0] += np.std(wednesday[0])
				wedstandarddevs[1] += np.std(wednesday[1])
				wedstandarddevs[2] += np.std(wednesday[2])
				wedcount += 1
			elif dayofweek == 'Thu':
				thursday[0] += np.array(correctedpings)
				pingstack[count] = np.array(correctedpings)
				thursday[1] += np.array(correctedjitters)
				jitterstack[count] = np.array(correctedjitters)
				thursday[2] += np.array(correctedlosses)
				lossstack = np.array(correctedlosses)
				thustandarddevs[0] += np.std(thursday[0])
				thustandarddevs[1] += np.std(thursday[1])
				thustandarddevs[2] += np.std(thursday[2])
				thucount += 1
			elif dayofweek == 'Fri':
				friday[0] += np.array(correctedpings)
				pingstack[count] = np.array(correctedpings)
				friday[1] += np.array(correctedjitters)
				jitterstack[count] = np.array(correctedjitters)
				friday[2] += np.array(correctedlosses)
				lossstack = np.array(correctedlosses)
				fristandarddevs[0] += np.std(friday[0])
				fristandarddevs[1] += np.std(friday[1])
				fristandarddevs[2] += np.std(friday[2])
				fricount += 1
			elif dayofweek == 'Sat':
				saturday[0] += np.array(correctedpings)
				pingstack[count] = np.array(correctedpings)
				saturday[1] += np.array(correctedjitters)
				jitterstack[count] = np.array(correctedjitters)
				saturday[2] += np.array(correctedlosses)
				lossstack = np.array(correctedlosses)
				satstandarddevs[0] += np.std(saturday[0])
				satstandarddevs[1] += np.std(saturday[1])
				satstandarddevs[2] += np.std(saturday[2])
				satcount += 1
			elif dayofweek == 'Sun':
				sunday[0] += np.array(correctedpings)
				pingstack[count] = np.array(correctedpings)
				sunday[1] += np.array(correctedjitters)
				jitterstack[count] = np.array(correctedjitters)
				sunday[2] += np.array(correctedlosses)
				lossstack = np.array(correctedlosses)
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


	for item in sessiondatalist:

		if item.date >= startdate and item.date <= enddate:
			timelen = len(item.times)
			locations = item.location

			#  Find session data
			itempings = item.pingtimes
			itemjitters = item.jitters
			itemlosses = item.losses
			itemdayofweek = item.dayofweek
			print itemdayofweek

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

				#  Pull same times from nosessionaverage list and standard deviations
				while i < 1440:
					if (reftimes[i] >= starttime) and (reftimes[i] <= endtime):
						nosessiontimes.append(reftimes[i])
						nosessionpings.append(nosessionaverage[0,i])
						nosessionjitters.append(nosessionaverage[1,i])
						nosessionlosses.append(nosessionaverage[2,i])

					i += 1

				#  Calculate statistics for ping times.
				itempingsaverage = np.mean(np.array(itempings))
				itempingsstd = np.std(np.array(itempings))
				nosessionpingsaverage = np.mean(np.array(nosessionpings))

				print itempingsaverage,itempingsstd,nosessionpingsaverage

				#  Calculate statistics for jitter.
				itemjittersaverage = np.mean(np.array(itemjitters))
				itemjittersstd = np.std(np.array(itemjitters))
				nosessionjittersaverage = np.mean(np.array(nosessionjitters))

				print itemjittersaverage,itemjittersstd,nosessionjittersaverage

				#  Calculate statistics for packet loss.
				itemlossesaverage = np.mean(np.array(itemlosses))
				itemlossesstd = np.std(np.array(itemlosses))
				nosessionlossesaverage = np.mean(np.array(nosessionlosses))

				print itemlossesaverage,itemlossesstd,nosessionlossesaverage


	return

def sortblackboxdata(datalist,sessiondatalist):

	schooldatalist = list()

	for school in blackboxschoollist:

		schoolitemlist = list()
		sessionslist = list()

		for item in datalist:
			locations = item.location
			itemschool = classtoschool[locations[0]]
			if itemschool == school:
				schoolitemlist.append(item)

		for item in sessiondatalist:
			itemschool = classtoschool[item.location[0]]
			if itemschool == school:
				sessionslist.append(item)


		if (schoolitemlist != []):
			graphdates(schoolitemlist,school,dt.datetime(2015,3,18),dt.datetime(2015,3,24))
			stackdays(schoolitemlist,sessionslist,school,dt.date(2015,3,18),dt.date(2015,3,24))

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
				location = item.location[0]				#### FIX THIS!!!!!!#####
				test = pullsessiondata(item,location)
				sessiondatalist.append(test)
		count += 1

	#  Plot data for each site.
	sortblackboxdata(datalist,sessiondatalist)

	return sessiondatalist