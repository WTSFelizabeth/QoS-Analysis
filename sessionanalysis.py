#  sessionanalysis.py
#  Created By:  Elizabeth Otto
#  Property Of: We Teach Science Foundation
#  Date Created:  11.17.14
#  Last Modified: 11.18.14
#  Description:  

from __future__ import division

import numpy as np
import scipy as sp
import scipy.stats as stats
import matplotlib as mpl
import matplotlib.pyplot as plt
import csv
import datetime as dt
import pylab

from pingdata import PingData
from surveydata import ClassSurveyData
from sessiondata import SessionStats

from pinganalysis import *
from surveyanalysis import *
from dictionaries import *
from pingfilelist import *

#  Split the survey list based on the date split indices from surveydatesplit, create a Session object.
def surveyobjectcreator(fullsurveyobject,begin,end, date):

	rooms = fullsurveyobject.rooms[begin:end]
	usernames = fullsurveyobject.usernames[begin:end]
	usertypes = fullsurveyobject.usertypes[begin:end]
	videos = fullsurveyobject.videos[begin:end]
	browsers = fullsurveyobject.browsers[begin:end]
	operatingsystems = fullsurveyobject.operatingsystems[begin:end]
	versions = fullsurveyobject.versions[begin:end]
	overalls = fullsurveyobject.overalls[begin:end]
	hearing = fullsurveyobject.hearing[begin:end]
	delays = fullsurveyobject.delays[begin:end]
	understandings = fullsurveyobject.understandings[begin:end]
	cuttings = fullsurveyobject.cuttings[begin:end]
	videoprobs = fullsurveyobject.videoprobs[begin:end]
	whiteboardprobs = fullsurveyobject.whiteboardprobs[begin:end]
	location = fullsurveyobject.location

	sessionObject = SessionSurveyData(date, rooms, usernames, usertypes, videos, browsers, operatingsystems, versions, overalls, hearing, delays, understandings, cuttings, videoprobs, whiteboardprobs, location)


	#  Return the Session Object to sessionanalysis
	return sessionObject

#  Detect split points based on date/location in the survey file so that the data can be split up by session
def surveydatesplit(surveylist):

	sessionObjectList = list()

	for item in surveylist:

		datestrlist = item.dates
		datelist = list()

		for entry in datestrlist:

			date = datefind(entry,2)
			datelist.append(date)

		indexlist = list()
		length = len(datelist)
		i = 1
		lastslice = 0

		while (i < length):
			
			if (datelist[i] == datelist[i-1]):
				i += 1

			else:
				objectdate = datelist[i-1]
				surveyobject = surveyobjectcreator(item,lastslice,i,objectdate)
				sessionObjectList.append(surveyobject)
				lastslice = i
				i += 1

	return sessionObjectList

#  Match session survey records to ping records.
def pingmatch(sessionObject, pingObjects, blackboxObjects):

	#  Define properties of the surveys.
	sessionloc = sessionObject.location
	sessionloc = classformatconvert[sessionloc]
	sessiondate = sessionObject.date

	matchlist1 = list()
	matchlist2 = list()

	#  Determine which (if any) ping files match the survey session.
	for item in pingObjects:

		pingloc = item.location
		pingdate = item.date

		if (pingloc == sessionloc) and (pingdate == sessiondate):
			matchlist1.append(item)

	#  Determine which (if any) blackbox session files match the survey session.
	for item in blackboxObjects:

		blackboxlocs = item.location
		blackboxdate = item.date

		for place in blackboxlocs:
			if (place == sessionloc) and (blackboxdate == sessiondate):
				matchlist2.append(item)

	return matchlist1,matchlist2

def sessiongraph(sessionObject, pingObjects, blackboxObjects):

	overallcount = sessionObject.countOveralls()
	location = sessionObject.location
	date = sessionObject.date.isoformat()
	number = str(len(sessionObject.overalls))

	times = list()
	pings = list()
	jitters = list()
	btimes = list()
	bpings = list()
	bjitters = list()
	blosses = list()
	bandwidth = 0

	for item in pingObjects:
		times.extend(item.times)
		pings.extend(item.pingtimes)
		jitters.extend(item.jitters)
		bandwidth = item.bandwidth

	for item in blackboxObjects:
		btimes.extend(item.times)
		bpings.extend(item.pingtimes)
		bjitters.extend(item.jitters)
		blosses.extend(item.losses)

	ind = np.array([0.5,1.5,2.5,3.5])
	width = 0.65

	fig = plt.figure()

	"""plt.subplot(221)
	plt.bar(ind,overallcount,width)
	plt.xticks(ind+width/2., ('Excellent', 'Good', 'Fair', 'Poor'))
	plt.axis([0,5,0,1])
	plt.title('Overall Survey Results')
	plt.ylabel('Proportion of Survey Respondents')"""

	ind = np.array([0.5,1.5,2.5,3.5,4.5,5.5])
	hearingcount, delaycount, understandingcount, cuttingcount, videocount, whiteboardcount = sessionObject.countProblems()
	width = 0.65

	"""littlelist = list()
	mediumlist = list()
	biglist = list()

	plt.subplot(222)
	littlelist.extend((hearingcount[1],delaycount[1],understandingcount[1],cuttingcount[1],videocount[1],whiteboardcount[1]))
	p1 = plt.bar(ind,littlelist,width,color = 'yellow')
	mediumlist.extend((hearingcount[2],delaycount[2],understandingcount[2],cuttingcount[2],videocount[2],whiteboardcount[2]))
	p2 = plt.bar(ind,mediumlist,width,color = 'orange',bottom=littlelist)
	biglist.extend((hearingcount[3],delaycount[3],understandingcount[3],cuttingcount[3],videocount[3],whiteboardcount[3]))
	p3 = plt.bar(ind,biglist,width,color = 'r',bottom =np.add(littlelist,mediumlist))
	yellow = mpl.patches.Patch(color = 'yellow', label = 'Small Interruption')
	orange = mpl.patches.Patch(color = 'orange', label = 'Large Interruption')
	red = mpl.patches.Patch(color = 'red', label = 'Session Could Not Continue')
	plt.legend(handles=[yellow,orange,red],prop={'size':8})
	plt.xticks(ind+width/2.,('Hearing','Delays','Understanding','Cutting','Video','Whiteboard'))
	plt.axis([0,6.5,0,1])
	plt.title('Reported Problems')
	plt.ylabel('Proportion of Survey Respondents')


	plt.subplot(223)
	if (pings != [] or bpings != []):
		plt.plot(times,pings,btimes,bpings)
		plt.gca().xaxis.set_major_formatter(mpl.dates.DateFormatter("%H:%M"))
		plt.title('Average Ping Times')
		plt.xlabel('Time')
		plt.ylabel('Average Ping Time (ms)')

	plt.subplot(224)
	if (jitters != [] or bjitters != []):
		plt.plot(times,jitters,btimes,bjitters)
		plt.gca().xaxis.set_major_formatter(mpl.dates.DateFormatter("%H:%M"))
		plt.title('Jitter')
		plt.xlabel('Time')
		plt.ylabel('Jitter (ms)')

	plt.suptitle(location + ' ' + date + '   N = ' + number, fontsize=20)

	fig.set_size_inches(18.5,10.5)

	fig.savefig(location+'_'+date)
	fig.clf()"""

	plt.close()

	return location,date,number,overallcount,hearingcount,delaycount,understandingcount,cuttingcount,videocount,whiteboardcount,pings,jitters,bandwidth,bpings,bjitters,blosses

def pearsonr(independent,dependent):

	i=0
	crosssum = 0
	xsum = 0
	ysum = 0
	points = len(independent)

	xbar = np.mean(independent)
	ybar = np.mean(dependent)

	while (i < points):

		a = (independent[i]-xbar)*(dependent[i]-ybar)
		crosssum += a

		b = (independent[i]-xbar)**2
		xsum += b

		c = (dependent[i]-ybar)**2
		ysum += c

		i += 1


	root1 = xsum**0.5
	root2 = ysum**0.5

	r = crosssum/(root1*root2)

	return r

def spearmanr(independent,dependent):

	rho = stats.spearmanr(independent,dependent)

	return rho

def chi2(independent,dependent,axes):

	r = 10
	c = 4
	nr = [0,0,0,0,0,0,0,0,0,0]
	nc = [0,0,0,0]

	levelsc = [0,1,2,3,4]
	rbottom = axes[0]
	rtop = axes[1]
	increment = (rtop-rbottom)/10
	levelsr = [0,increment,increment*2,increment*3,increment*4,increment*5,increment*6,increment*7,increment*8,increment*9,increment*10]

	i = 0
	j = 0

	while (i < r):
		bottom = levelsr[i]
		top = levelsr[i+1]

		for item in independent:
			if (item > bottom) and (item < top):
				nr[i] += 1

		i += 1

	while (j < c):
		bottom = levelsc[j]
		top = levelsc[j+1]

		for item in dependent:
			if (item > bottom) and (item < top):
				nc[j] += 1

		j += 1

	Erc = np.zeros((4,10))
	Orc = np.zeros((4,10))

	i = 0
	j = 0
	n = len(independent)

	while (i < r):
		while (j < c):
			nrnc = nr[i]*nc[j]/n
			Erc[j,i]=nrnc
			j += 1
		i += 1
		j = 0

	i = 0
	j = 0
	k = 0

	while (i < n):

		ind = independent[i]
		dep = dependent[i]

		while (j < r):
			bottomr = levelsr[j]
			topr = levelsr[j+1]

			while (k < c):
				bottomc = levelsc[k]
				topc = levelsc[k+1]

				if (bottomr < ind) and (topr > ind) and (bottomc < dep) and (topc > dep):
					Orc[k,j] += 1

				k += 1

			k = 0
			j += 1

		j = 0
		i += 1


	i = 0
	j = 0
	k = 0
	chi2val = 0
	DF = 0 

	while (i < r):
		while (j <c):
			if (Erc[j,i] != 0):
				diff = Orc[j,i] - Erc[j,i]
				square = diff**2
				term = square/Erc[j,i]
				chi2val += term
				DF += 1
			j += 1
		i += 1

	pvalue = 1 - stats.chi2.cdf(chi2val,DF)

	return pvalue

def graphfunction(x,y,axes,xlabel,ylabel,colorcode = False,locs=list()):

	if (colorcode == False):
		r = round(pearsonr(x,y),3)
		s = 'r = ' + str(r)
		rho = round(spearmanr(x,y)[0],3)
		pval = 'p = ' + str(round(chi2(x,y,axes),3))
		plt.plot(x,y,'ro')
		plt.axis(axes)
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.text(axes[1]/1.25,0.5,s,fontdict = None)
		plt.text(axes[1]/1.25,0.8,r'$\rho$ = ' + str(rho),fontdict = None)
		plt.text(axes[1]/1.25,1.1,pval,fontdict = None)

	else:
		schools = list()
		r = round(pearsonr(x,y),3)
		s = 'r = ' + str(r)
		rho = round(spearmanr(x,y)[0],3)
		pval = 'p = ' + str(round(chi2(x,y,axes),3))

		i = 0
		while i < len(locs):
			schools.append(classtoschool[locs[i]])
			i += 1

		i = 0
		while i < len(locs):
			if (schools[i] == 'IBL'):
				plt.plot(x[i],y[i],'ro',ms=9)
				i += 1
			elif (schools[i] == 'Sierramont'):
				plt.plot(x[i],y[i],'mv',ms=9)
				i += 1
			elif (schools[i] == 'Piedmont'):
				plt.plot(x[i],y[i],'g8',ms=9)
				i += 1
			elif (schools[i] == 'SLHS'):
				plt.plot(x[i],y[i],'cs',ms=9)
				i += 1
			elif (schools[i] == 'Nimitz'):
				plt.plot(x[i],y[i],'k^',ms=9)
				i += 1
			else:
				plt.plot(x[i],y[i],'b>',ms=9)
				i += 1

		plt.axis(axes)
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.text(axes[1]/1.25,0.5,s,fontdict = None)
		plt.text(axes[1]/1.25,0.8,r'$\rho$ = ' + str(rho),fontdict = None)
		plt.text(axes[1]/1.25,1.1,pval,fontdict = None)

	return

def metricsgraph(locations,dates,numbers,overallmetrics,hearingmetrics,delaymetrics,understandingmetrics,cuttingmetrics,videometrics,whiteboardmetrics,averagepings,
	averagepingstdevs,maxminpings,averagejitters,bandwidths):
	
	## Average Ping Metrics ##
	fig = plt.figure()

	xtitle = 'Average Ping Time (ms)'
	axes = [0,110,0,4.1]

	plt.subplot(321)
	graphfunction(averagepings,overallmetrics,axes,xtitle,'Overall Quality Metric',colorcode=False,locs=locations)
#	plt.errorbar(averagepings,overallmetrics,xerr=averagepingstdevs,color="black",linestyle="None")

	plt.subplot(322)
	graphfunction(averagepings,hearingmetrics,axes,xtitle,'Hearing Patner Metric',colorcode=False,locs=locations)
#	plt.errorbar(averagepings,hearingmetrics,xerr=averagepingstdevs,color="black",linestyle="None")

	plt.subplot(323)
	graphfunction(averagepings,delaymetrics,axes,xtitle,'Delays in Audio Metric',colorcode=False,locs=locations)

	plt.subplot(324)
	graphfunction(averagepings,understandingmetrics,axes,xtitle,'Understanding Partner Metric',colorcode=False,locs=locations)

	plt.subplot(325)
	graphfunction(averagepings,cuttingmetrics,axes,xtitle,'Audio Cutting In and Out Metric',colorcode=False,locs=locations)

	plt.subplot(326)
	graphfunction(averagepings,whiteboardmetrics,axes,xtitle,'Whiteboard Functionality Metric',colorcode=False,locs=locations)

	plt.suptitle('Metrics Compared to Average Ping Time', fontsize=20)

	fig.set_size_inches(18.5,10.5)
	fig.savefig('Pings_vs_Metrics')

	fig.clf()
	plt.close()

	## Max-Min Ping Metrics ##
	fig = plt.figure()

	xtitle = 'Variation in Ping Time (Max-Min) (ms)'
	axes = [0,700,0,4.1]

	plt.subplot(321)
	graphfunction(maxminpings,overallmetrics,axes,xtitle,'Overall Quality Metric',colorcode=False,locs=locations)

	plt.subplot(322)
	graphfunction(maxminpings,hearingmetrics,axes,xtitle,'Hearing Partner Metric',colorcode=False,locs=locations)

	plt.subplot(323)
	graphfunction(maxminpings,delaymetrics,axes,xtitle,'Delays in Audio Metric',colorcode=False,locs=locations)

	plt.subplot(324)
	graphfunction(maxminpings,understandingmetrics,axes,xtitle,'Understanding Partner Metric',colorcode=False,locs=locations)

	plt.subplot(325)
	graphfunction(maxminpings,cuttingmetrics,axes,xtitle,'Audio Cutting In and Out Metric',colorcode=False,locs=locations)

	plt.subplot(326)
	graphfunction(maxminpings,whiteboardmetrics,axes,xtitle,'Whiteboard Functionality Metric',colorcode=False,locs=locations)

	plt.suptitle('Metrics Compared to Variation in Ping Time', fontsize=20)

	fig.set_size_inches(18.5,10.5)
	fig.savefig('VariationsinPings_vs_Metrics')

	fig.clf()
	plt.close()

	## Average Jitter Metrics ##
	fig = plt.figure()

	xtitle = 'Average Jitter (ms)'
	axes = [0,100,0,4.1]

	plt.subplot(321)
	graphfunction(averagejitters,overallmetrics,axes,xtitle,'Overall Quality Metric',colorcode=False,locs=locations)

	plt.subplot(322)
	graphfunction(averagejitters,hearingmetrics,axes,xtitle,'Hearing Partner Metric',colorcode=False,locs=locations)

	plt.subplot(323)
	graphfunction(averagejitters,delaymetrics,axes,xtitle,'Delays in Audio Metric',colorcode=False,locs=locations)

	plt.subplot(324)
	graphfunction(averagejitters,understandingmetrics,axes,xtitle,'Understanding Partner Metric',colorcode=False,locs=locations)

	plt.subplot(325)
	graphfunction(averagejitters,cuttingmetrics,axes,xtitle,'Audio Cutting In and Out Metric',colorcode=False,locs=locations)

	plt.subplot(326)
	graphfunction(averagejitters,whiteboardmetrics,axes,xtitle,'Whiteboard Functionality Metric',colorcode=False,locs=locations)

	plt.suptitle('Metrics Compared to Average Jitter', fontsize=20)

	fig.set_size_inches(18.5,10.5)
	fig.savefig('Jitters_vs_Metrics')

	fig.clf()
	plt.close()

	## Standard Deviation Metrics ##

	fig = plt.figure()

	xtitle = 'Standard Deviation of Average Ping Time (ms)'
	axes = [0,25,0,4.1]

	plt.subplot(321)
	graphfunction(averagepingstdevs,overallmetrics,axes,xtitle,'Overall Quality Metric',colorcode=False,locs=locations)

	plt.subplot(322)
	graphfunction(averagepingstdevs,hearingmetrics,axes,xtitle,'Hearing Partner Metric',colorcode=False,locs=locations)

	plt.subplot(323)
	graphfunction(averagepingstdevs,delaymetrics,axes,xtitle,'Delays in Audio Metric',colorcode=False,locs=locations)

	plt.subplot(324)
	graphfunction(averagepingstdevs,understandingmetrics,axes,xtitle,'Understanding Partner Metric',colorcode=False,locs=locations)

	plt.subplot(325)
	graphfunction(averagepingstdevs,cuttingmetrics,axes,xtitle,'Audio Cutting In and Out Metric',colorcode=False,locs=locations)

	plt.subplot(326)
	graphfunction(averagepingstdevs,whiteboardmetrics,axes,xtitle,'Whiteboard Functionality Metric',colorcode=False,locs=locations)

	plt.suptitle('Metrics Compared to Standard Deviation of Average Ping Time', fontsize=20)

	fig.set_size_inches(18.5,10.5)
	fig.savefig('Stdevs_vs_Metrics')

	fig.clf()
	plt.close()

	## Bandwidth Metrics ##

	fig = plt.figure()

	xtitle = 'Bandwidth (kbps)'
	axes = [0,22000,0,4.1]

	plt.subplot(321)
	graphfunction(bandwidths,overallmetrics,axes,xtitle,'Overall Quality Metric',colorcode=False,locs=locations)

	plt.subplot(322)
	graphfunction(bandwidths,hearingmetrics,axes,xtitle,'Hearing Partner Metric',colorcode=False,locs=locations)

	plt.subplot(323)
	graphfunction(bandwidths,delaymetrics,axes,xtitle,'Delays in Audio Metric',colorcode=False,locs=locations)

	plt.subplot(324)
	graphfunction(bandwidths,understandingmetrics,axes,xtitle,'Understanding Partner Metric',colorcode=False,locs=locations)

	plt.subplot(325)
	graphfunction(bandwidths,cuttingmetrics,axes,xtitle,'Audio Cutting In and Out Metric',colorcode=False,locs=locations)

	plt.subplot(326)
	graphfunction(bandwidths,whiteboardmetrics,axes,xtitle,'Whiteboard Functionality Metric',colorcode=False,locs=locations)

	plt.suptitle('Metrics Compared to Bandwidth', fontsize=20)

	fig.set_size_inches(18.5,10.5)
	fig.savefig('Bandwidth_vs_Metrics')

	fig.clf()
	plt.close()

	return

def sessionanalysis(surveylist,pinglist,blackboxsessionlist):

	sessionObjectList = surveydatesplit(surveylist)
	sessionStatsList = list()
	pinglengthtot = 0

	for item in sessionObjectList:

		matchlist,blackboxmatchlist = pingmatch(item, pinglist, blackboxsessionlist)
		
		location,date,number,overallcount,hearingcount,delaycount,understandingcount,cuttingcount,videocount,whiteboardcount,pings,jitters,bandwidth,bpings,bjitters,blosses = sessiongraph(item, matchlist, blackboxmatchlist)

		sessionStats = SessionStats(location, date, number, overallcount, hearingcount, delaycount, understandingcount, cuttingcount, videocount, whiteboardcount, pings, jitters, bandwidth,bpings,bjitters,blosses)

		sessionStatsList.append(sessionStats)

		pinglengthtot += len(pings)

	pingaverage = str(pinglengthtot/len(sessionStatsList))
	print 'Average Length of Ping Test = ' + pingaverage + ' minutes'

	locations = list()
	dates = list()
	numbers = list()
	overallmetrics = list()
	hearingmetrics = list()
	delaymetrics = list()
	understandingmetrics = list()
	cuttingmetrics = list()
	videometrics = list()
	whiteboardmetrics = list()
	averagepings = list()
	averagepingstdevs = list()
	maxminpings = list()
	averagejitters = list()
	bandwidths = list()
	completions = list()
	noofsessions = 0

	for item in sessionStatsList:

		## Filter out the surveys with no matching ping record, those used for testing, and those with less than 3 entries from a session. ##
		if (item.pings != [] and item.location != 'Testing' and float(item.number) >= 3):
			locations.append(item.location)
			dates.append(item.date)
			numbers.append(item.number)
			overallmetrics.append(item.overallmetric())
			hearingmetric,delaymetric,understandingmetric,cuttingmetric,videometric,whiteboardmetric = item.problemmetrics()
			hearingmetrics.append(hearingmetric)
			delaymetrics.append(delaymetric)
			understandingmetrics.append(understandingmetric)
			cuttingmetrics.append(cuttingmetric)
			videometrics.append(videometric)
			whiteboardmetrics.append(whiteboardmetric)
			averagepings.append(item.averageping())
			averagepingstdevs.append(item.averagepingstdev())
			maxminpings.append(item.maxminping())
			averagejitters.append(item.averagejitter())
			bandwidths.append(item.bandwidth)
			completions.append(item.completion())
			noofsessions += 1

	print 'Number of Sessions = ' + str(noofsessions)
	completionaverage = str(np.mean(completions))
	print 'Completion Average = ' + completionaverage

	#  Graph and analyze metrics vs. measures of connection quality, etc.
	metricsgraph(locations,dates,numbers,overallmetrics,hearingmetrics,delaymetrics,understandingmetrics,cuttingmetrics,videometrics,whiteboardmetrics,
	averagepings,averagepingstdevs,maxminpings,averagejitters,bandwidths)

	return	