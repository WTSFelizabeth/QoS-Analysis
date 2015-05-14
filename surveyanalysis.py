#  surveyanalysis.py
#  Created By:  Elizabeth Otto
#  Property Of: We Teach Science Foundation
#  Date Created:  10.13.14
#  Last Modified: 03.17.15
#  Description:  

from __future__ import division

import numpy as np
import scipy as sp
import matplotlib as mpl
import csv

from surveydata import *
from dictionaries import classlist, classtoschool, schoollist, overallratingslist, propertyratingslist
from acdictionaries import acclasslist

######  Sort through surveys to find those at the desired location.  ######
def surveyfindclass(dates, rooms, usernames, usertypes, locations, videos, browsers, operatingsystems, versions, overalls, hearing, delays, understandings, cuttings, videoprobs, whiteboardprobs, desiredlocation):

	a = list()
	b = list()
	c = list()
	d = list()
	e = list()
	f = list()
	g = list()
	h = list()
	i = list()
	j = list()
	k = list()
	l = list()
	m = list()
	n = list()
	o = list()

	count = 0

	for entry in locations:
		if (entry == desiredlocation):
			a.append(dates[count])
			b.append(rooms[count])
			c.append(usernames[count])
			d.append(usertypes[count])
			e.append(videos[count])
			f.append(browsers[count])
			g.append(operatingsystems[count])
			h.append(versions[count])
			i.append(overalls[count])
			j.append(hearing[count])
			k.append(delays[count])
			l.append(understandings[count])
			m.append(cuttings[count])
			n.append(videoprobs[count])
			o.append(whiteboardprobs[count])

			count += 1
		else:
			count += 1

	return a,b,c,d,e,f,g,h,i,j,k,l,m,n,o

######  Sort surveys by the desired class and create a class data object.  ######
def surveysortclass(dates, rooms, usernames, usertypes, locations, videos, browsers, operatingsystems, versions, overalls, hearing, delays, understandings, cuttings, videoprobs, whiteboardprobs, desiredlocation):

	dates, rooms, usernames, usertypes, videos, browsers, operatingsystems, versions, overalls, hearing, delays, understandings, cuttings, videoprobs, whiteboardprobs = surveyfindclass(dates, rooms, 
		usernames, usertypes, locations, videos, browsers, operatingsystems, versions, overalls, hearing, delays, understandings, cuttings, videoprobs, whiteboardprobs, desiredlocation)

	classData = ClassSurveyData(dates, rooms, usernames, usertypes, videos, browsers, operatingsystems, versions, overalls, hearing, delays, understandings, cuttings, videoprobs, whiteboardprobs, desiredlocation)

	return classData

######  Sort surveys by the desired school and create a school data object.  ######
def surveysortschool(classDataList, desiredschool):

	dates = list()
	rooms = list()
	usernames = list()
	usertypes = list()
	locations = list()
	videos = list()
	browsers = list()
	operatingsystems = list()
	versions = list()
	overalls = list()
	hearing = list()
	delays = list()
	understandings = list()
	cuttings = list()
	videoprobs = list()
	whiteboardprobs = list()

	for entry in classDataList:

		school = entry.school

		if (school == desiredschool):

			dates.extend(entry.dates)
			rooms.extend(entry.rooms)
			usernames.extend(entry.usernames)
			usertypes.extend(entry.usertypes)
			videos.extend(entry.videos)
			browsers.extend(entry.browsers)
			operatingsystems.extend(entry.operatingsystems)
			versions.extend(entry.versions)
			overalls.extend(entry.overalls)
			hearing.extend(entry.hearing)
			delays.extend(entry.delays)
			understandings.extend(entry.understandings)
			cuttings.extend(entry.cuttings)
			videoprobs.extend(entry.videoprobs)
			whiteboardprobs.extend(entry.whiteboardprobs)

	schoolData = SchoolSurveyData(dates, rooms, usernames, usertypes, videos, browsers, operatingsystems, versions, overalls, hearing, delays, understandings, cuttings, videoprobs, whiteboardprobs, desiredschool)

	return schoolData

######  Check for and correct user type error from beginning of the year - Internet Explorer.  ######
def checkusertype(usertype,browser):

	if (usertype == '' and browser == 'internet explorer'):
		usertypestr = 'mentor'
	else:
		usertypestr = usertype

	return usertypestr

######  Calculate p_bad - defined as probability of a fair or poor experience on a particular metric.  ######
def badprobcalc(metric):

	#  Set an index.

	totalbad = metric[2]+metric[3]

	probbad = totalbad

	return probbad

######  Graph problem metrics by operating system.  ######
def graphos(windowslist,osxlist,chromelist,metricname):

	#  Establish graphing variables
	fig = plt.figure()

	width = 0.65
	ind = np.array([0.5,1.5,2.5,3.5])

	labels = ('None','Minor','Major','Session Ended')
	plt.suptitle('Network Type Results - ' + metricname,fontsize=20)


	windowsmetric = np.array(problemCount(windowslist))
	osxmetric = np.array(problemCount(osxlist))
	chromemetric = np.array(problemCount(chromelist))

	#  Graph Windows
	plt.subplot(311)
	plt.bar(ind,windowsmetric,width,color='green')
	plt.xticks(ind+width/2.,labels)
	plt.title('Windows Results')
	plt.ylabel('Proportion of Respondents')
	plt.axis([0,4.5,0,0.7])
	probbadw = badprobcalc(windowsmetric)
	plt.text(3.5,0.6,r'p$_{bad}$ = '+str(round(probbadw,3)))

	#  Graph OS X
	plt.subplot(312)
	plt.bar(ind,osxmetric,width,color='blue')
	plt.xticks(ind+width/2.,labels)
	plt.title('OS X Results')
	plt.ylabel('Proportion of Respondents')
	plt.axis([0,4.5,0,0.7])
	probbado = badprobcalc(osxmetric)
	plt.text(3.5,0.6,r'p$_{bad}$ = '+str(round(probbado,3)))

	#  Graph Chromebooks
	plt.subplot(313)
	plt.bar(ind,chromemetric,width,color='purple')
	plt.xticks(ind+width/2.,labels)
	plt.title('Chrome OS Results')
	plt.ylabel('Proportion of Respondents')
	plt.axis([0,4.5,0,0.7])
	probbadc = badprobcalc(chromemetric)
	plt.text(3.5,0.6,r'p$_{bad}$ = '+str(round(probbadc,3)))

	#  Set save condiitons
	fig.set_size_inches(8.5,11)
	fig.savefig('OS_'+metricname)

	#  Close the figure
	fig.clf()
	plt.close()

	return

######  Graph problem metrics by network type.  ######
def graphnetworktype(wiredlist,wirelesslist,metricname):

	#  Calculate metrics from lists.
	wiredmetric = np.array(problemCount(wiredlist))
	wirelessmetric = np.array(problemCount(wirelesslist))

	#  Establish graphing variables.
	fig = plt.figure()

	width = 0.65
	ind = np.array([0.5,1.5,2.5,3.5])
	labels = ('None','Minor','Major','Session Ended')
	plt.suptitle('Network Type Results - ' + metricname,fontsize=20)

	#  Graph wired.
	plt.subplot(311)
	plt.bar(ind,wiredmetric,width,color='green')
	plt.xticks(ind+width/2.,labels)
	plt.title('Wired Results')
	plt.ylabel('Proportion of Respondents')
	plt.axis([0,4.5,0,0.7])
	probbad1 = badprobcalc(wiredmetric)
	plt.text(3.5,0.6,r'p$_{bad}$ = '+str(round(probbad1,3)))

	#  Graph wireless.
	plt.subplot(312)
	plt.bar(ind,wirelessmetric,width,color='blue')
	plt.xticks(ind+width/2.,labels)
	plt.title('Wireless Results')
	plt.ylabel('Proportion of Respondents')
	plt.axis([0,4.5,0,0.7])
	probbad2 = badprobcalc(wirelessmetric)
	plt.text(3.5,0.6,r'p$_{bad}$ = '+str(round(probbad2,3)))

	#  Graph diff.
	plt.subplot(313)
	plt.bar(ind,(wiredmetric-wirelessmetric),width,color='black')
	plt.xticks(ind+width/2.,labels)
	plt.title('Differences in Wired and Wireless Results')
	plt.ylabel('Wired Proportion - Wireless Proportion')
	plt.axis([0,4.5,-0.2,0.2])
	plt.axhline(linewidth=2,color='black')
	deltaprobbad = probbad1-probbad2
	plt.text(3.5,0.15,r'$\Delta$p$_{bad}$ = '+str(round(deltaprobbad,3)))


	#  Set save conditions.
	fig.set_size_inches(8.5,11)
	fig.savefig('NetworkType_'+metricname)

	#  Close figure.
	fig.clf()
	plt.close()

	return

def sortedgraphs(classDataList):
	windowslist = list()
	osxlist = list()
	chromelist = list()

	wiredlist = list()
	wirelesslist = list()

	for item in classDataList:
		if item.studentos == 'Windows':
			windowslist.append(item)
		elif item.studentos == 'OS X':
			osxlist.append(item)
		elif item.studentos == 'Chromebook':
			chromelist.append(item)

		if item.network == 'wired':
			wiredlist.append(item)
		elif item.network == 'wireless':
			wirelesslist.append(item)

	windowsoveralls = list()
	windowshearing = list()
	windowsdelays = list()
	windowsunderstandings = list()
	windowscuttings = list()
	windowswhiteboardprobs = list()

	for item in windowslist:
		windowsoveralls.extend(item.overalls)
		windowshearing.extend(item.hearing)
		windowsdelays.extend(item.delays)
		windowsunderstandings.extend(item.understandings)
		windowscuttings.extend(item.cuttings)
		windowswhiteboardprobs.extend(item.whiteboardprobs)

	osxoveralls = list()
	osxhearing = list()
	osxdelays = list()
	osxunderstandings = list()
	osxcuttings = list()
	osxwhiteboardprobs = list()

	for item in osxlist:
		osxoveralls.extend(item.overalls)
		osxhearing.extend(item.hearing)
		osxdelays.extend(item.delays)
		osxunderstandings.extend(item.understandings)
		osxcuttings.extend(item.cuttings)
		osxwhiteboardprobs.extend(item.whiteboardprobs)


	chromeoveralls = list()
	chromehearing = list()
	chromedelays = list()
	chromeunderstandings = list()
	chromecuttings = list()
	chromewhiteboardprobs = list()

	for item in chromelist:
		chromeoveralls.extend(item.overalls)
		chromehearing.extend(item.hearing)
		chromedelays.extend(item.delays)
		chromeunderstandings.extend(item.understandings)
		chromecuttings.extend(item.cuttings)
		chromewhiteboardprobs.extend(item.whiteboardprobs)

	wiredoveralls = list()
	wiredhearing = list()
	wireddelays = list()
	wiredunderstandings = list()
	wiredcuttings = list()
	wiredwhiteboardprobs = list()

	for item in wiredlist:
		wiredoveralls.extend(item.overalls)
		wiredhearing.extend(item.hearing)
		wireddelays.extend(item.delays)
		wiredunderstandings.extend(item.understandings)
		wiredcuttings.extend(item.cuttings)
		wiredwhiteboardprobs.extend(item.whiteboardprobs)


	wirelessoveralls = list()
	wirelesshearing = list()
	wirelessdelays = list()
	wirelessunderstandings = list()
	wirelesscuttings = list()
	wirelesswhiteboardprobs = list()

	for item in wirelesslist:
		wirelessoveralls.extend(item.overalls)
		wirelesshearing.extend(item.hearing)
		wirelessdelays.extend(item.delays)
		wirelessunderstandings.extend(item.understandings)
		wirelesscuttings.extend(item.cuttings)
		wirelesswhiteboardprobs.extend(item.whiteboardprobs)

	#  Calculate number of relevant responses for each meaure (OS/network type).
	windowsn = len(windowsoveralls)
	osxn = len(osxoveralls)
	chromen = len(chromeoveralls)
	wiredn = len(wiredoveralls)
	wirelessn = len(wirelessoveralls)

	#  Print numbers to terminal for now.
	print 'Number of respondents where student OS = Windows: '+str(windowsn)
	print 'Number of respondents where student OS = OS X: '+str(osxn)
	print 'Number of respondents where student OS = Chromebook: '+str(chromen)
	print 'Number of respondents where student network is wired: '+str(wiredn)
	print 'Number of respondents where student network is wireless: '+str(wirelessn)

	#  Graph metrics by student OS.

	fig = plt.figure()

	width = 0.65
	ind = np.array([0.5,1.5,2.5,3.5])

	windowsoverallmetrics = np.array(overallCount(windowsoveralls))/len(windowsoveralls)
	osxoverallmetrics = np.array(overallCount(osxoveralls))/len(osxoveralls)
	chromeoverallmetrics = np.array(overallCount(chromeoveralls))/len(chromeoveralls)

	#  Windows Overall
	plt.subplot(311)
	plt.bar(ind,windowsoverallmetrics,width,color='green')
	plt.xticks(ind+width/2.,('Excellent','Good','Fair','Poor'))
	plt.title('Windows Results')
	plt.ylabel('Proportion of Respondents')
	plt.axis([0,4.5,0,0.7])
	probbadw = badprobcalc(windowsoverallmetrics)
	plt.text(3.5,0.6,r'p$_{bad}$ = '+str(round(probbadw,3)))

	#  OSX Overall
	plt.subplot(312)
	plt.bar(ind,osxoverallmetrics,width,color='blue')
	plt.xticks(ind+width/2.,('Excellent','Good','Fair','Poor'))
	plt.title('OS X Results')
	plt.ylabel('Proportion of Respondents')
	plt.axis([0,4.5,0,0.7])
	probbado = badprobcalc(osxoverallmetrics)
	plt.text(3.5,0.6,r'p$_{bad}$ = '+str(round(probbado,3)))

	#  Chromebook Overall
	plt.subplot(313)
	plt.bar(ind,chromeoverallmetrics,width,color='purple')
	plt.xticks(ind+width/2.,('Excellent','Good','Fair','Poor'))
	plt.title('Chrome OS Results')
	plt.ylabel('Proportion of Respondents')
	plt.axis([0,4.5,0,0.7])
	probbadc = badprobcalc(chromeoverallmetrics)
	plt.text(3.5,0.6,r'p$_{bad}$ = '+str(round(probbadc,3)))


	fig.set_size_inches(8.5,11)
	fig.savefig('OS_Overall')

	fig.clf()
	plt.close()

	#  Plot individual metrics.
	graphos(windowshearing,osxhearing,chromehearing,'Problems Hearing Partner')
	graphos(windowsdelays,osxdelays,chromedelays,'Delayed Audio')
	graphos(windowsunderstandings,osxunderstandings,chromeunderstandings,'Problems Understanding Partner')
	graphos(windowscuttings,osxcuttings,chromecuttings,'Audio Cutting Out')
	graphos(windowswhiteboardprobs,osxwhiteboardprobs,chromewhiteboardprobs,'Problems with Whiteboard')

	#  Graph metrics by student network type.

	fig = plt.figure()

	width = 0.65
	ind = np.array([0.5,1.5,2.5,3.5])

	wiredoverallmetrics = np.array(overallCount(wiredoveralls))/len(wiredoveralls)
	wirelessoverallmetrics = np.array(overallCount(wirelessoveralls))/len(wirelessoveralls)

	#  Wired Overall
	plt.subplot(311)
	plt.bar(ind,wiredoverallmetrics,width,color='green')
	plt.xticks(ind+width/2.,('Excellent','Good','Fair','Poor'))
	plt.title('Wired Results')
	plt.ylabel('Proportion of Respondents')
	plt.axis([0,4.5,0,0.7])
	probbad1 = badprobcalc(wiredoverallmetrics)
	plt.text(3.5,0.6,r'p$_{bad}$ = '+str(round(probbad1,3)))

	#  Wireless Overall
	plt.subplot(312)
	plt.bar(ind,wirelessoverallmetrics,width,color='blue')
	plt.xticks(ind+width/2.,('Excellent','Good','Fair','Poor'))
	plt.title('Wireless Results')
	plt.ylabel('Proportion of Respondents')
	plt.axis([0,4.5,0,0.7])
	probbad2 = badprobcalc(wirelessoverallmetrics)
	plt.text(3.5,0.6,r'p$_{bad}$ = '+str(round(probbad2,3)))

	# Diff Overall
	plt.subplot(313)
	plt.bar(ind,(wiredoverallmetrics-wirelessoverallmetrics),width,color='black')
	plt.xticks(ind+width/2.,('Excellent','Good','Fair','Poor'))
	plt.title('Differences in Wired and Wireless Results')
	plt.ylabel('Wired Proportion - Wireless Proportion')
	plt.axis([0,4.5,-0.2,0.2])
	plt.axhline(linewidth=2,color='black')
	deltaprobbad = probbad1-probbad2
	plt.text(3.5,0.15,r'$\Delta$p$_{bad}$ = '+str(round(deltaprobbad,3)))

	fig.set_size_inches(8.5,11)
	fig.savefig('NetworkType_Overall')

	fig.clf()
	plt.close()

	#  Plot individual metrics.
	graphnetworktype(wiredhearing,wirelesshearing,'Problems Hearing Partner')
	graphnetworktype(wireddelays,wirelessdelays,'Delayed Audio')
	graphnetworktype(wiredunderstandings,wirelessunderstandings,'Problems Understanding Partner')
	graphnetworktype(wiredcuttings,wirelesscuttings,'Audio Cutting Out')
	graphnetworktype(wiredwhiteboardprobs,wirelesswhiteboardprobs,'Problems with Whiteboard')

	return

######  Import the data from surveys.txt.  ######
def surveyimport(file):

	#  Create a list for each data field in the survey.
	count = 0
	dates = list()
	rooms = list()
	usernames = list()
	usertypes = list()
	locations = list()
	videos = list()
	browsers = list()
	operatingsystems = list()
	versions = list()
	overalls = list()
	hearing = list()
	delays = list()
	understandings = list()
	cuttings = list()
	videoprobs = list()
	whiteboardprobs = list()

	#  Open the csv file.
	with open(file, 'rb') as csvfile:
		filereader = csv.reader(csvfile)

		for line in filereader:
			
			#  Skip the first line in the file (which has field names) + first 5 lines (which have old data)
			if (count < 6):
				count += 1

			#  Read in the rest of the file.
			else:
				datestr = line[0]
				dates.append(datestr)

				roomstr = line[1]
				rooms.append(roomstr)

				usernamestr = line[2]
				usernames.append(usernamestr)

				#  Import usertype and browser simultaneously to check for errors in user type.
				usertypestr = line[3]
				browserstr = line[6]
				usertypestr = checkusertype(usertypestr, browserstr)
				usertypes.append(usertypestr)

				locationstr = line[4]
				locations.append(locationstr)

				videostr = line[5]
				videos.append(videostr)

				browserstr = line[6]
				browsers.append(browserstr)
				
				osstr = line[7]
				operatingsystems.append(osstr)

				versionstr = line[8]
				versions.append(versionstr)

				overallstr = line[9]
				overalls.append(overallstr)

				hearingstr = line[10]
				hearing.append(hearingstr)

				delaystr = line[11]
				delays.append(delaystr)

				understandingstr = line[12]
				understandings.append(understandingstr)

				cuttingstr = line[13]
				cuttings.append(cuttingstr)
				
				videoprobstr = line[14]
				videoprobs.append(videoprobstr)

				whiteboardprobstr = line[15]
				whiteboardprobs.append(whiteboardprobstr)

				count += 1

	return dates, rooms, usernames, usertypes, locations, videos, browsers, operatingsystems, versions, overalls, hearing, delays, understandings, cuttings, videoprobs, whiteboardprobs

######  Feed survey data to various analysis functions, then return class data list for session analysis.  ######
def surveycontroller(filename):

	#  Import the full set of survey results.
	dates, rooms, usernames, usertypes, locations, videos, browsers, operatingsystems, versions, overalls, hearing, delays, understandings, cuttings, videoprobs, whiteboardprobs = surveyimport(filename)

	#  Create a full survey object.
	fullData = FullSurveyData(dates, usernames, usertypes, locations, videos, browsers, operatingsystems, versions, overalls, hearing, delays, understandings, cuttings, videoprobs, whiteboardprobs)
	fullData.osTabulate()
	fullData.surveyOverTime()
	fullData.countRespondents()
	fullData.aggregateSurvey()

	#  Sort the surveys by class - creating one object for each class and adding to a list.
	classDataList = list()

	for entry in classlist:
		classData = surveysortclass(dates, rooms, usernames, usertypes, locations, videos, browsers, operatingsystems, versions, overalls, hearing, delays, understandings, cuttings, videoprobs, whiteboardprobs, entry)
		classDataList.append(classData)

	acCompList = list()

	# Pull comparison classes for AC pilot.
	for entry in acclasslist:
		for item in classDataList:
			location = item.location
			if entry == location:
				acCompList.append(item)

	sortedgraphs(classDataList)

	#  Sort the surveys by school - creating one object for each school and adding to a list.
	schoolDataList = list()

	fig = plt.figure()
	number = 330

	#  Loop over school list
	for entry in schoollist:

		schoolData = surveysortschool(classDataList,entry)

		if (entry != 'Cabrillo') and (entry != 'Columbia') and (entry != 'Testing') and (entry != 'Horn') and (entry != 'RL Turner'):
			number = number + 1
			plt.subplot(number)
			schoolData.surveyOverTime()
			schoolData.surveyPlotSchool()

		schoolDataList.append(schoolData)


	fig.set_size_inches(20.5,10.5)
	fig.savefig('Surveys_Over_Time')

	fig.clf()
	plt.close()

	plt.close()

	return classDataList, acCompList

def questioncorrelations(data):

	#  Create numpy arrays for each correlation.
	overallvhearing = np.zeros((4,4))
	overallvdelay = np.zeros((4,4))
	overallvunderstanding = np.zeros((4,4))
	overallvcutting = np.zeros((4,4))
	overallvwhiteboard = np.zeros

	overall = data.overalls
	hearing = data.hearing
	delay = data.delays
	understanding = data.understandings
	cutting = data.cuttings
	whiteboard = data.whiteboardprobs

	i = 0

	for overallitem in overall:

		hearingitem = hearing[i]
		delayitem = delay[i]
		understandingitem = understanding[i]
		cuttingitem = cutting[i]
		whiteboarditem = whiteboard[i]
		print overallitem,hearingitem,delayitem,understandingitem,cuttingitem,whiteboarditem

		if overallitem == 'Excellent':
			index = 0
		elif overallitem == 'Good':
			index = 1
		elif overallitem == 'Fair':
			index = 2
		elif overallitem == 'Poor':
			index = 3

		if hearingitem == 'none':
			indexh = 0
		elif hearingitem == 'small':
			indexh = 1
		elif hearingitem == 'large':
			indexh = 2
		elif hearingitem == 'worst':
			indexh = 3

		if understandingitem == 'none':
			indexu = 0
		elif understandingitem == 'small':
			indexu = 1
		elif understandingitem == 'large':
			indexu = 2
		elif understandingitem == 'worst':
			indexu = 3

		overallvhearing[index,indexh] += 1
		overallvunderstanding[index,indexu] += 1
		i += 1

	print overallvhearing, overallvunderstanding

	return

def acsurveycontroller(filename,accomplist):

	dates, rooms, usernames, usertypes, locations, videos, browsers, operatingsystems, versions, overalls, hearing, delays, understandings, cuttings, videoprobs, whiteboardprobs = surveyimport(filename)

	#  Create a full survey object.
	fullACData = ACFullSurveyData(dates, usernames, usertypes, locations, videos, browsers, operatingsystems, versions, overalls, hearing, delays, understandings, cuttings, videoprobs, whiteboardprobs)
	fullACData.aggregateSurvey()

	#  Sort the AC surveys by class
	ACclassDataList = list()

	#  AC survey question correlations.
	questioncorrelations(fullACData)

	#  Creat plots for each AC class.
	for entry in acclasslist:
		classData = surveysortclass(dates, rooms, usernames, usertypes, locations, videos, browsers, operatingsystems, versions, overalls, hearing, delays, understandings, cuttings, videoprobs, whiteboardprobs, entry)
		ACclassDataList.append(classData)
		if classData.overalls != []:
			acoveralls,achearings,acdelays,acunderstandings,accuttings,acwhiteboards = classData.acPlotAggregate()
		for item in accomplist:
			if item.location == entry:
				compoveralls,comphearings,compdelays,compunderstandings,compcuttings,compwhiteboards = item.acPlotAggregate(flag = True)

		diffoveralls = acoveralls - compoveralls
		diffhearings = achearings - comphearings
		diffdelays = acdelays - compdelays
		diffunderstandings = acunderstandings - compunderstandings
		diffcuttings = accuttings - compcuttings
		diffwhiteboards = acwhiteboards - compwhiteboards
		
	#  Add diff graphing/calculations here.

	#  Add averaging over class here.
	return