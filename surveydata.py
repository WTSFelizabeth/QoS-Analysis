#  surveydata.py
#  Created By:  Elizabeth Otto
#  Property Of: We Teach Science Foundation
#  Date Created:  10.13.14
#  Last Modified: 10.13.14
#  Description:  

from __future__ import division

import datetime as dt
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt

from dictionaries import classtoschool
from dictionaries import overallratings, propertyratings
from dictionaries import oslist
from dictionaries import months
from dictionaries import classtostudentos, classtonetwork
from sessiondata import problemaverage

def overallCount(overalls):

	countlist = [0,0,0,0]

	for entry in overalls:

		rating = overallratings[entry]
		
		if (rating == 1):
			countlist[3] += 1
		elif (rating == 2):
			countlist[2] += 1
		elif (rating == 3):
			countlist[1] += 1
		elif (rating == 4):
			countlist[0] += 1 

	return countlist

def problemCount(propertylist):

	countlist = [0,0,0,0]

	length = len(propertylist)

	for entry in propertylist:

		rating = propertyratings[entry]
		
		if (rating == 1):
			countlist[3] += 1
		elif (rating == 2):
			countlist[2] += 1
		elif (rating == 3):
			countlist[1] += 1
		elif (rating == 4):
			countlist[0] += 1

	i = 0
	while (i < 4):
		countlist[i] = float(countlist[i])/float(length)
		i += 1

	return countlist

def badprobcalc(metric):

	#  Set an index.

	totalbad = metric[2]+metric[3]

	probbad = totalbad

	return probbad

def osGraph(windows,osx,chromebook,labels,title):

	ind = np.array([0.5,1.5,2.5])
	width = 0.65

	nonelist = list()
	littlelist = list()
	mediumlist = list()
	biglist = list()

	nonelist.extend((windows[0],osx[0],chromebook[0]))
	littlelist.extend((windows[1],osx[1],chromebook[1]))
	mediumlist.extend((windows[2],osx[2],chromebook[2]))
	biglist.extend((windows[3],osx[3],chromebook[3]))

	p0 = plt.bar(ind,nonelist,width,color='g')
	p1 = plt.bar(ind,littlelist,width,color = 'yellow',bottom = nonelist)
	p2 = plt.bar(ind,mediumlist,width,color = 'orange',bottom = np.add(nonelist,littlelist))
	p3 = plt.bar(ind,biglist,width,color = 'r',bottom = np.add(mediumlist,np.add(nonelist,littlelist)))
	green = mpl.patches.Patch(color = 'green', label = labels[0])
	yellow = mpl.patches.Patch(color = 'yellow', label = labels[1])
	orange = mpl.patches.Patch(color = 'orange', label = labels[2])
	red = mpl.patches.Patch(color = 'red', label = labels[3])
	plt.legend(handles=[green,yellow,orange,red], prop={'size':8},loc=4)
	plt.xticks(ind+width/2.,('Windows','OS X','Chromebook'))
	plt.axis([0,3.5,0,1])
	plt.title(title)
	plt.ylabel('Proportion of OS Users')

	return

class FullSurveyData():

	def __init__(self, dates, usernames, usertypes, locations, videos, browsers, operatingsystems, versions, overalls, hearing, delays, understandings, cuttings, videoprobs, whiteboardprobs):

		#  Link data to the object.
		self.dates = dates
		self.usernames = usernames
		self.usertypes = usertypes
		self.locations = locations
		self.videos = videos
		self.browsers = browsers
		self.operatingsystems = operatingsystems
		self.versions = versions
		self.overalls = overalls
		self.hearing = hearing
		self.delays = delays
		self.understandings = understandings
		self.cuttings = cuttings
		self.videoprobs = videoprobs
		self.whiteboardprobs = whiteboardprobs

	def countSurveys(self):
		surveycount = len(self.overalls)
		return surveycount

	def countRespondents(self):

		length = len(self.usernames)
		userlist = list()

		studentlist = list()
		studentoveralls = list()
		studenthearing = list()
		studentdelays = list()
		studentunderstandings = list()
		studentcuttings = list()
		studentwhiteboardprobs = list()

		mentorlist = list()
		mentoroveralls = list()
		mentorhearing = list()
		mentordelays = list()
		mentorunderstandings = list()
		mentorcuttings = list()
		mentorwhiteboardprobs = list()

		excellentlist = list()
		goodlist = list()
		fairlist = list()
		poorlist = list()

		usertypelist = list()
		i = 0

		while (i < length):
			if (self.locations[i] != 'Testing'):
				userlist.append(self.usernames[i])
				usertypelist.append(self.usertypes[i])

				if (self.overalls[i] == 'Excellent'):
					excellentlist.append(self.usernames[i])
				elif (self.overalls[i] == 'Good'):
					goodlist.append(self.usernames[i])
				elif (self.overalls[i] == 'Fair'):
					fairlist.append(self.usernames[i])
				elif (self.overalls[i] == 'Poor'):
					poorlist.append(self.usernames[i])

			if (self.usertypes[i] == 'student'):
				studentlist.append(self.usernames[i])
				studentoveralls.append(self.overalls[i])
				studenthearing.append(self.hearing[i])
				studentdelays.append(self.delays[i])
				studentunderstandings.append(self.understandings[i])
				studentcuttings.append(self.cuttings[i])
				studentwhiteboardprobs.append(self.whiteboardprobs[i])
			if (self.usertypes[i] == 'mentor'):
				mentorlist.append(self.usernames[i])
				mentoroveralls.append(self.overalls[i])
				mentorhearing.append(self.hearing[i])
				mentordelays.append(self.delays[i])
				mentorunderstandings.append(self.understandings[i])
				mentorcuttings.append(self.cuttings[i])
				mentorwhiteboardprobs.append(self.whiteboardprobs[i])

			i += 1

		totalresponses = str(len(userlist))
		uniqueresponses = str(len(set(userlist)))

		print 'Total Number of Responses = ' + totalresponses
		print 'Total Unique Respondents = ' + uniqueresponses

		mentortotal = len(mentorlist)
		studenttotal = len(studentlist) 

		print 'Total Mentor Responses = ' + str(mentortotal)
		print 'Total Student Responses = ' + str(studenttotal)

		mentorresponses = len(set(mentorlist))
		studentresponses = len(set(studentlist))

		totalexcellents = len(excellentlist)
		uniqueexcellents = len(set(excellentlist))
		excellentratio = str(uniqueexcellents/totalexcellents)

		print 'Ratio of Unique/Total for Excellent Rating = '+ excellentratio

		totalgoods = len(goodlist)
		uniquegoods = len(set(goodlist))
		goodratio = uniquegoods/totalgoods

		totalfairs = len(fairlist)
		uniquefairs = len(set(fairlist))
		fairratio = uniquefairs/totalfairs

		totalpoors = len(poorlist)
		uniquepoors = len(set(poorlist))
		poorratio = str(uniquepoors/totalpoors)

		print 'Ratio of Unique/Total for Poor Rating = ' + poorratio

		mentoroverallcount = np.array(overallCount(mentoroveralls))/mentortotal
		moverallmetric = problemaverage(mentoroverallcount,1)
		studentoverallcount = np.array(overallCount(studentoveralls))/studenttotal
		soverallmetric = problemaverage(studentoverallcount,1)

		mentorhearingcount = problemCount(mentorhearing)
		mhearingmetric = problemaverage(mentorhearingcount,1)
		studenthearingcount = problemCount(studenthearing)
		shearingmetric = problemaverage(studenthearingcount,1)

		mentordelaycount = problemCount(mentordelays)
		mdelaymetric = problemaverage(mentordelaycount,1)
		studentdelaycount = problemCount(studentdelays)
		sdelaymetric = problemaverage(studentdelaycount,1)

		mentorunderstandingcount = problemCount(mentorunderstandings)
		munderstandingmetric = problemaverage(mentorunderstandingcount,1)
		studentunderstandingcount = problemCount(studentunderstandings)
		sunderstandingmetric = problemaverage(studentunderstandingcount,1)

		mentorcuttingcount = problemCount(mentorcuttings)
		mcuttingmetric = problemaverage(mentorcuttingcount,1)
		studentcuttingcount = problemCount(studentcuttings)
		scuttingmetric = problemaverage(studentcuttingcount,1)

		mentorwhiteboardcount = problemCount(mentorwhiteboardprobs)
		mwhiteboardmetric = problemaverage(mentorwhiteboardcount,1)
		studentwhiteboardcount = problemCount(studentwhiteboardprobs)
		swhiteboardmetric = problemaverage(studentwhiteboardcount,1)

		fig = plt.figure()

		ind = np.array([0.5,1.5,2.5,3.5,4.5,5.5])
		width = 0.65
		mentormetrics = np.array([moverallmetric,mhearingmetric,mdelaymetric,munderstandingmetric,mcuttingmetric,mwhiteboardmetric])
		studentmetrics = np.array([soverallmetric,shearingmetric,sdelaymetric,sunderstandingmetric,scuttingmetric,swhiteboardmetric])

		plt.subplot(311)
		plt.bar(ind,mentormetrics,width,color='green')
		plt.xticks(ind+width/2.,('Overall','Hearing','Delays','Understanding','Cutting','Whiteboard'))
		plt.title('Mentor Results')
		plt.ylabel('Metric (Mentors Only)')
		plt.axis([0,6.5,0,4])

		plt.subplot(312)
		plt.bar(ind,studentmetrics,width,color='blue')
		plt.xticks(ind+width/2.,('Overall','Hearing','Delays','Understanding','Cutting','Whiteboard'))
		plt.title('Student Results')
		plt.ylabel('Metric (Students Only)')
		plt.axis([0,6.5,0,4])

		plt.subplot(313)
		plt.bar(ind,(mentormetrics-studentmetrics),width,color='black')
		plt.xticks(ind+width/2.,('Overall','Hearing','Delays','Understanding','Cutting','Whiteboard'))
		plt.title('Differences in Mentor and Student Results')
		plt.ylabel('Mentor Metric - Student Metric')
		plt.axis([0,6.5,-1,1])
		plt.axhline(linewidth=2,color='black')


		fig.set_size_inches(8.5,11)
		fig.savefig('Student_vs_Mentor')

		fig.clf()
		plt.close()

		return

	def osTabulate(self):

		length = len(self.operatingsystems)
		i = 0
		oscounts = [0,0,0]

		windowsoveralls = list()
		windowshearing = list()
		windowsdelays = list()
		windowsunderstandings = list()
		windowscuttings = list()
		windowswhiteboard = list()

		osxoveralls = list()
		osxhearing = list()
		osxdelays = list()
		osxunderstandings = list()
		osxcuttings = list()
		osxwhiteboard = list()

		chromebookoveralls = list()
		chromebookhearing = list()
		chromebookdelays = list()
		chromebookunderstandings = list()
		chromebookcuttings = list()
		chromebookwhiteboard = list()

		while i < length:

			if (self.operatingsystems[i] == oslist[0]):
				oscounts[0] += 1
				windowsoveralls.append(self.overalls[i])
				windowshearing.append(self.hearing[i])
				windowsdelays.append(self.delays[i])
				windowsunderstandings.append(self.understandings[i])
				windowscuttings.append(self.cuttings[i])
				windowswhiteboard.append(self.whiteboardprobs[i])

			elif (self.operatingsystems[i] == oslist[1]):
				oscounts[1] += 1
				osxoveralls.append(self.overalls[i])
				osxhearing.append(self.hearing[i])
				osxdelays.append(self.delays[i])
				osxunderstandings.append(self.understandings[i])
				osxcuttings.append(self.cuttings[i])
				osxwhiteboard.append(self.whiteboardprobs[i])


			elif (self.operatingsystems[i] == oslist[2]):
				oscounts[2] += 1
				chromebookoveralls.append(self.overalls[i])
				chromebookhearing.append(self.hearing[i])
				chromebookdelays.append(self.delays[i])
				chromebookunderstandings.append(self.understandings[i])
				chromebookcuttings.append(self.cuttings[i])
				chromebookwhiteboard.append(self.whiteboardprobs[i])

			i += 1

		i = 0
		windowscounts = overallCount(windowsoveralls)
		osxcounts = overallCount(osxoveralls)
		chromebookcounts = overallCount(chromebookoveralls)

		windowshearingcounts = problemCount(windowshearing)
		osxhearingcounts = problemCount(osxhearing)
		chromebookhearingcounts = problemCount(chromebookhearing)

		windowsdelayscounts = problemCount(windowsdelays)
		osxdelayscounts = problemCount(osxdelays)
		chromebookdelayscounts = problemCount(chromebookdelays)

		windowsunderstandingscounts = problemCount(windowsunderstandings)
		osxunderstandingscounts = problemCount(osxunderstandings)
		chromebookunderstandingscounts = problemCount(chromebookunderstandings)

		windowscuttingscounts = problemCount(windowscuttings)
		osxcuttingscounts = problemCount(osxcuttings)
		chromebookcuttingscounts = problemCount(chromebookcuttings)

		windowswhiteboardcounts = problemCount(windowswhiteboard)
		osxwhiteboardcounts = problemCount(osxwhiteboard)
		chromebookwhiteboardcounts = problemCount(chromebookwhiteboard)

		while i < 4:

			windowscounts[i] = windowscounts[i]/oscounts[0]
			osxcounts[i] = osxcounts[i]/oscounts[1]
			chromebookcounts[i] = chromebookcounts[i]/oscounts[2]

			i += 1

		fig = plt.figure()

		plt.subplot(321)
		labels = ['Excellent','Good','Fair','Poor']
		title = 'Overall Quality of Session by Operating System'
		osGraph(windowscounts,osxcounts,chromebookcounts,labels,title)

		plt.subplot(322)
		labels = ['No Issue','Small Interruption','Large Interruption','Session Could Not Continue']
		title = 'Hearing Partner by Operating System'
		osGraph(windowshearingcounts,osxhearingcounts,chromebookhearingcounts,labels,title)

		plt.subplot(323)
		title = 'Delays in Audio by Operating System'
		osGraph(windowsdelayscounts,osxdelayscounts,chromebookdelayscounts,labels,title)

		plt.subplot(324)
		title = 'Understanding Partner by Operating System'
		osGraph(windowsunderstandingscounts,osxunderstandingscounts,chromebookunderstandingscounts,labels,title)

		plt.subplot(325)
		title = 'Audio Cutting In and Out by Operating System'
		osGraph(windowscuttingscounts,osxcuttingscounts,chromebookcuttingscounts,labels,title)

		plt.subplot(326)
		title = 'Whiteboard Problems by Operating System'
		osGraph(windowswhiteboardcounts,osxwhiteboardcounts,chromebookwhiteboardcounts,labels,title)

		fig.set_size_inches(18.5,10.5)

		fig.savefig('Surveys_vs_OS')

		fig.clf()

		plt.close()

		return

	def surveyOverTime(self):

		overalllist = list()
		length = len(self.dates)
		i = 0
		octtot = 0
		novtot = 0
		dectot = 0
		jantot = 0
		febtot = 0
		martot = 0
		aprtot = 0
		octcount = 0
		novcount = 0
		deccount = 0
		jancount = 0
		febcount = 1
		marcount = 1
		aprcount = 1

		while (i < length):
			if (self.overalls[i] != '') and (self.locations[i] != 'Testing'):
				
				splitstr = self.dates[i].split('_')
				newsplit = splitstr[0].split('-')
				month = months[newsplit[1]]

				if (month == 10):
					rating = overallratings[self.overalls[i]]
					octtot += rating
					octcount += 1
				elif (month == 11):
					rating = overallratings[self.overalls[i]]
					novtot += rating
					novcount += 1
				elif (month == 12):
					rating = overallratings[self.overalls[i]]
					dectot += rating
					deccount += 1
				elif (month == 1):
					rating = overallratings[self.overalls[i]]
					jantot += rating
					jancount += 1	
				elif (month == 2):
					rating = overallratings[self.overalls[i]]
					febtot += rating
					febcount += 1
				elif (month == 3):
					rating = overallratings[self.overalls[i]]
					martot += rating
					marcount += 1
				elif (month == 4):
					rating = overallratings[self.overalls[i]]
					aprtot += rating
					aprcount += 1									
			i += 1

		october = octtot/octcount
		november = novtot/novcount
		december = dectot/deccount
		january = jantot/jancount
		february = febtot/febcount
		march = martot/marcount
		april = aprtot/aprcount

		ind = np.array([0.5,1.5,2.5,3.5,4.5,5.5,6.5])
		width = 0.65
		plt.bar(ind,[october,november,december,january,february,march,april],width)
		plt.axis([0,7.5,0,4])
		plt.xticks(ind+width/2., ('October', 'November', 'December', 'January','February','March','April'))
		plt.title('Overall Survey Results Over Time')
		plt.ylabel('Average Overall Survey Rating')
		plt.show()

		plt.close()	

		return

	def aggregateSurvey(self):

		length = len(self.overalls)
		overallist = list()
		hearinglist = list()
		delayslist = list()
		understandingslist = list()
		cuttingslist = list()
		whiteboardlist = list()
		i = 0

		while (i < length):
			if (self.overalls[i] != ''):
				overallist.append(self.overalls[i])
			if (self.hearing[i] != ''):
				hearinglist.append(self.hearing[i])
			if (self.delays[i] != ''):
				delayslist.append(self.delays[i])
			if (self.understandings[i] != ''):
				understandingslist.append(self.understandings[i])
			if (self.cuttings[i] != ''):
				cuttingslist.append(self.cuttings[i])
			if (self.whiteboardprobs[i] != ''):
				whiteboardlist.append(self.whiteboardprobs[i])

			i += 1

		overalltab = np.array(overallCount(overallist))
		overallratings = overalltab/length

		hearingratings = np.array(problemCount(hearinglist))
		delaysratings = np.array(problemCount(delayslist))
		understandingsratings = np.array(problemCount(understandingslist))
		cuttingsratings = np.array(problemCount(cuttingslist))
		whiteboardratings = np.array(problemCount(whiteboardlist))

		fig = plt.figure()

		plt.subplot(321)
		ind = np.array([0.5,1.5,2.5,3.5])
		width = 0.65
		plt.bar(ind,overallratings, width,color='green')
		plt.axis([0,4.5,0,0.7])
		plt.xticks(ind+width/2.,('Excellent','Good','Fair','Poor'))
		plt.title('Survey Q1: Overall Experience')
		plt.ylabel('Proportion of Respondents')
		prob = badprobcalc(overallratings)
		plt.text(3.5,0.6,r'p$_{bad}$ = '+str(round(prob,3)))

		plt.subplot(322)
		plt.bar(ind,hearingratings,width,color = 'blue')
		plt.axis([0,4.5,0,0.7])
		plt.xticks(ind+width/2.,('No Problems','Minor Problems','Major Problems','Session Stopped'))
		plt.title('Survey Q2: Hearing Your Partner')
		plt.ylabel('Proportion of Respondents')
		prob = badprobcalc(hearingratings)
		plt.text(3.5,0.6,r'p$_{bad}$ = '+str(round(prob,3)))


		plt.subplot(323)
		plt.bar(ind,delaysratings,width)
		plt.axis([0,4.5,0,0.7])
		plt.xticks(ind+width/2.,('No Problems','Minor Problems','Major Problems','Session Stopped'))
		plt.title('Survey Q3: Delays in Audio')
		plt.ylabel('Proportion of Respondents')
		prob = badprobcalc(delaysratings)
		plt.text(3.5,0.6,r'p$_{bad}$ = '+str(round(prob,3)))

		plt.subplot(324)
		plt.bar(ind,understandingsratings,width)
		plt.axis([0,4.5,0,0.7])
		plt.xticks(ind+width/2.,('No Problems','Minor Problems','Major Problems','Session Stopped'))
		plt.title('Survey Q4: Understanding Your Partner')
		plt.ylabel('Proportion of Respondents')
		prob = badprobcalc(understandingsratings)
		plt.text(3.5,0.6,r'p$_{bad}$ = '+str(round(prob,3)))

		plt.subplot(325)
		plt.bar(ind,cuttingsratings,width)
		plt.axis([0,4.5,0,0.7])
		plt.xticks(ind+width/2.,('No Problems','Minor Problems','Major Problems','Session Stopped'))
		plt.title('Survey Q5: Sound Cutting In and Out')
		plt.ylabel('Proportion of Respondents')
		prob = badprobcalc(cuttingsratings)
		plt.text(3.5,0.6,r'p$_{bad}$ = '+str(round(prob,3)))

		plt.subplot(326)
		plt.bar(ind,whiteboardratings,width,color = 'orange')
		plt.axis([0,4.5,0,0.7])
		plt.xticks(ind+width/2.,('No Problems','Minor Problems','Major Problems','Session Stopped'))
		plt.title('Survey Q6: Whiteboard Functionality')
		plt.ylabel('Proportion of Respondents')
		prob = badprobcalc(whiteboardratings)
		plt.text(3.5,0.6,r'p$_{bad}$ = '+str(round(prob,3)))


		plt.suptitle('Aggregate Survey Results', fontsize=20)

		fig.set_size_inches(18.5,10.5)

		fig.savefig('Aggregate_Surveys')
		fig.clf()

		plt.close()
		return


class ClassSurveyData():

	def __init__(self, dates, rooms, usernames, usertypes, videos, browsers, operatingsystems, versions, overalls, hearing, delays, understandings, cuttings, videoprobs, whiteboardprobs, location):

		#  Link data to the object.
		self.dates = dates
		self.rooms = rooms
		self.usernames = usernames
		self.usertypes = usertypes
		self.videos = videos
		self.browsers = browsers
		self.operatingsystems = operatingsystems
		self.versions = versions
		self.overalls = overalls
		self.hearing = hearing
		self.delays = delays
		self.understandings = understandings
		self.cuttings = cuttings
		self.videoprobs = videoprobs
		self.whiteboardprobs = whiteboardprobs

		#  Define the location
		self.location = location
		self.school = classtoschool[location]

		#  Define location network characteristics
		self.studentos = classtostudentos[self.location]
		self.network = classtonetwork[self.location]

	def countLocationSurveys(self):
		surveycount = len(self.overalls)
		return surveycount

	def acPlotAggregate(self,flag = False):

		length = len(self.overalls)
		overallist = list()
		hearinglist = list()
		delayslist = list()
		understandingslist = list()
		cuttingslist = list()
		whiteboardlist = list()
		i = 0

		while (i < length):
			if (self.overalls[i] != ''):
				overallist.append(self.overalls[i])
			if (self.hearing[i] != ''):
				hearinglist.append(self.hearing[i])
			if (self.delays[i] != ''):
				delayslist.append(self.delays[i])
			if (self.understandings[i] != ''):
				understandingslist.append(self.understandings[i])
			if (self.cuttings[i] != ''):
				cuttingslist.append(self.cuttings[i])
			if (self.whiteboardprobs[i] != ''):
				whiteboardlist.append(self.whiteboardprobs[i])

			i += 1

		overalltab = np.array(overallCount(overallist))
		overallratings = overalltab/length

		hearingratings = np.array(problemCount(hearinglist))
		delaysratings = np.array(problemCount(delayslist))
		understandingsratings = np.array(problemCount(understandingslist))
		cuttingsratings = np.array(problemCount(cuttingslist))
		whiteboardratings = np.array(problemCount(whiteboardlist))

		fig = plt.figure()

		plt.subplot(321)
		ind = np.array([0.5,1.5,2.5,3.5])
		width = 0.65
		plt.bar(ind,overallratings, width,color='green')
		plt.axis([0,4.5,0,1.0])
		plt.xticks(ind+width/2.,('Excellent','Good','Fair','Poor'))
		plt.title('Survey Q1: Overall Experience')
		plt.ylabel('Proportion of Respondents')
		prob = badprobcalc(overallratings)
		plt.text(3.5,0.85,r'p$_{bad}$ = '+str(round(prob,3)))

		plt.subplot(322)
		plt.bar(ind,hearingratings,width,color = 'blue')
		plt.axis([0,4.5,0,1.0])
		plt.xticks(ind+width/2.,('No Problems','Minor Problems','Major Problems','Session Stopped'))
		plt.title('Survey Q2: Hearing Your Partner')
		plt.ylabel('Proportion of Respondents')
		prob = badprobcalc(hearingratings)
		plt.text(3.5,0.85,r'p$_{bad}$ = '+str(round(prob,3)))

		plt.subplot(323)
		plt.bar(ind,delaysratings,width)
		plt.axis([0,4.5,0,1.0])
		plt.xticks(ind+width/2.,('No Problems','Minor Problems','Major Problems','Session Stopped'))
		plt.title('Survey Q3: Delays in Audio')
		plt.ylabel('Proportion of Respondents')
		prob = badprobcalc(delaysratings)
		plt.text(3.5,0.85,r'p$_{bad}$ = '+str(round(prob,3)))

		plt.subplot(324)
		plt.bar(ind,understandingsratings,width)
		plt.axis([0,4.5,0,1.0])
		plt.xticks(ind+width/2.,('No Problems','Minor Problems','Major Problems','Session Stopped'))
		plt.title('Survey Q4: Understanding Your Partner')
		plt.ylabel('Proportion of Respondents')
		prob = badprobcalc(understandingsratings)
		plt.text(3.5,0.85,r'p$_{bad}$ = '+str(round(prob,3)))

		plt.subplot(325)
		plt.bar(ind,cuttingsratings,width)
		plt.axis([0,4.5,0,1.0])
		plt.xticks(ind+width/2.,('No Problems','Minor Problems','Major Problems','Session Stopped'))
		plt.title('Survey Q5: Sound Cutting In and Out')
		plt.ylabel('Proportion of Respondents')
		prob = badprobcalc(cuttingsratings)
		plt.text(3.5,0.85,r'p$_{bad}$ = '+str(round(prob,3)))

		plt.subplot(326)
		plt.bar(ind,whiteboardratings,width,color = 'orange')
		plt.axis([0,4.5,0,1.0])
		plt.xticks(ind+width/2.,('No Problems','Minor Problems','Major Problems','Session Stopped'))
		plt.title('Survey Q6: Whiteboard Functionality')
		plt.ylabel('Proportion of Respondents')
		prob = badprobcalc(whiteboardratings)
		plt.text(3.5,0.85,r'p$_{bad}$ = '+str(round(prob,3)))

		if flag == False:
			plt.suptitle('Adobe Connect - Aggregate Survey Results - '+self.location+'  N = '+str(length), fontsize = 20)
		elif flag == True:
			plt.suptitle('Adobe Connect - Comparison Survey Results - '+self.location+'  N = '+str(length), fontsize = 20)

		fig.set_size_inches(18.5,10.5)

		if flag == False:
			fig.savefig('AC_Aggregate_Surveys_'+self.location)
		elif flag == True:
			fig.savefig('AC_Aggregate_Comp_'+self.location)
		fig.clf()

		plt.close()

		return overallratings,hearingratings,delaysratings,understandingsratings,cuttingsratings,whiteboardratings


class SessionSurveyData():

	def __init__(self, date, rooms, usernames, usertypes, videos, browsers, operatingsystems, versions, overalls, hearing, delays, understandings, cuttings, videoprobs, whiteboardprobs, location):

		#  Link date to object.
		self.rooms = rooms
		self.usernames = usernames
		self.usertypes = usertypes
		self.videos = videos
		self.browsers = browsers
		self.operatingsystems = operatingsystems
		self.versions = versions
		self.overalls = overalls
		self.hearing = hearing
		self.delays = delays
		self.understandings = understandings
		self.cuttings = cuttings
		self.videoprobs = videoprobs
		self.whiteboardprobs = whiteboardprobs

		#  Define the class, school and date.
		self.date = date
		self.location = location
		self.school = classtoschool[location]

	def countLocationSurveys(self):
		surveycount = len(self.overalls)
		return surveycount

	def countOveralls(self):
		overallcount = overallCount(self.overalls)
		surveycount = len(self.overalls)
		overallnormalized = list()

		for item in overallcount:

			item = float(item)/float(surveycount)
			overallnormalized.append(item)

		return overallnormalized

	def countProblems(self):

		a = 1

		hearingcount = problemCount(self.hearing)
		delaycount = problemCount(self.delays)
		understandingcount = problemCount(self.understandings)
		cuttingcount = problemCount(self.cuttings)
		videocount = problemCount(self.videoprobs)
		whiteboardcount = problemCount(self.whiteboardprobs)

		return hearingcount, delaycount, understandingcount, cuttingcount, videocount, whiteboardcount
		

class SchoolSurveyData():

	def __init__(self, dates, rooms, usernames, usertypes, videos, browsers, operatingsystems, versions, overalls, hearing, delays, understandings, cuttings, videoprobs, whiteboardprobs, school):

		#  Link data to the object.
		self.dates = dates
		self.rooms = rooms
		self.usernames = usernames
		self.usertypes = usertypes
		self.videos = videos
		self.browsers = browsers
		self.operatingsystems = operatingsystems
		self.versions = versions
		self.overalls = overalls
		self.hearing = hearing
		self.delays = delays
		self.understandings = understandings
		self.cuttings = cuttings
		self.videoprobs = videoprobs
		self.whiteboardprobs = whiteboardprobs

		#  Define the school.
		self.school = school


	def countSchoolSurveys(self):
		surveycount = len(self.overalls)
		return surveycount

	def surveyOverTime(self):

		overalllist = list()
		length = len(self.dates)
		i = 0
		octtot = 0
		novtot = 0
		dectot = 0
		jantot = 0
		febtot = 0
		martot = 0
		aprtot = 0
		octcount = 0
		novcount = 0
		deccount = 0
		jancount = 0
		febcount = 0
		marcount = 0
		aprcount = 0

		while (i < length):
			if (self.overalls[i] != '') and (self.school != 'Testing'):
				
				splitstr = self.dates[i].split('_')
				newsplit = splitstr[0].split('-')
				month = months[newsplit[1]]

				if (month == 10):
					rating = overallratings[self.overalls[i]]
					octtot += rating
					octcount += 1
				elif (month == 11):
					rating = overallratings[self.overalls[i]]
					novtot += rating
					novcount += 1
				elif (month == 12):
					rating = overallratings[self.overalls[i]]
					dectot += rating
					deccount += 1
				elif (month == 1):
					rating = overallratings[self.overalls[i]]
					jantot += rating
					jancount += 1
				elif (month == 2):
					rating = overallratings[self.overalls[i]]
					febtot += rating
					febcount += 1
				elif (month == 3):
					rating = overallratings[self.overalls[i]]
					martot += rating
					marcount += 1
				elif (month == 4):
					rating = overallratings[self.overalls[i]]
					aprtot += rating
					aprcount += 1										
			i += 1

		if (octcount != 0):
			october = octtot/octcount
		else:
			october = 0
		if (novcount != 0):
			november = novtot/novcount
		else:
			november = 0
		if (deccount != 0):
			december = dectot/deccount
		else:
			december = 0
		if (jancount != 0):
			january = jantot/jancount
		else:
			january = 0
		if (febcount != 0):
			february = febtot/febcount
		else:
			february = 0
		if (marcount != 0):
			march = martot/marcount
		else:
			march = 0
		if (aprcount != 0):
			april = aprtot/aprcount
		else:
			april = 0

		if (october != 0 or november != 0 or december != 0 or january != 0 or february != 0 or march != 0 or april != 0):
			ind = np.array([0.5,1.5,2.5,3.5,4.5,5.5,6.5])
			width = 0.65
			plt.bar(ind,[october,november,december,january,february,march,april],width)
			plt.axis([0,7.5,0,4])
			plt.xticks(ind+width/2., ('Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr'))
			plt.title('Overall Survey Results Over Time - '+self.school)
			plt.ylabel('Average Overall Survey Rating')

	def surveyPlotSchool(self):

		length = len(self.overalls)
		overallist = list()
		hearinglist = list()
		delayslist = list()
		understandingslist = list()
		cuttingslist = list()
		whiteboardlist = list()
		i = 0

		while (i < length):
			if (self.overalls[i] != ''):
				overallist.append(self.overalls[i])
			if (self.hearing[i] != ''):
				hearinglist.append(self.hearing[i])
			if (self.delays[i] != ''):
				delayslist.append(self.delays[i])
			if (self.understandings[i] != ''):
				understandingslist.append(self.understandings[i])
			if (self.cuttings[i] != ''):
				cuttingslist.append(self.cuttings[i])
			if (self.whiteboardprobs[i] != ''):
				whiteboardlist.append(self.whiteboardprobs[i])

			i += 1

		overalltab = np.array(overallCount(overallist))
		length = len(overallist)
		overallratings = overalltab/length

		hearingratings = np.array(problemCount(hearinglist))
		delaysratings = np.array(problemCount(delayslist))
		understandingsratings = np.array(problemCount(understandingslist))
		cuttingsratings = np.array(problemCount(cuttingslist))
		whiteboardratings = np.array(problemCount(whiteboardlist))

		fig = plt.figure()

		plt.subplot(321)
		ind = np.array([0.5,1.5,2.5,3.5])
		width = 0.65
		plt.bar(ind,overallratings, width,color='green')
		plt.axis([0,4.5,0,0.8])
		plt.xticks(ind+width/2.,('Excellent','Good','Fair','Poor'))
		plt.title('Survey Q1: Overall Experience')
		plt.ylabel('Proportion of Respondents')
		prob = badprobcalc(overallratings)
		plt.text(3.5,0.7,r'p$_{bad}$ = '+str(round(prob,3)))

		plt.subplot(322)
		plt.bar(ind,hearingratings,width,color = 'blue')
		plt.axis([0,4.5,0,0.8])
		plt.xticks(ind+width/2.,('No Problems','Minor Problems','Major Problems','Session Stopped'))
		plt.title('Survey Q2: Hearing Your Partner')
		plt.ylabel('Proportion of Respondents')
		prob = badprobcalc(hearingratings)
		plt.text(3.5,0.7,r'p$_{bad}$ = '+str(round(prob,3)))

		plt.subplot(323)
		plt.bar(ind,delaysratings,width)
		plt.axis([0,4.5,0,0.8])
		plt.xticks(ind+width/2.,('No Problems','Minor Problems','Major Problems','Session Stopped'))
		plt.title('Survey Q3: Delays in Audio')
		plt.ylabel('Proportion of Respondents')
		prob = badprobcalc(delaysratings)
		plt.text(3.5,0.7,r'p$_{bad}$ = '+str(round(prob,3)))

		plt.subplot(324)
		plt.bar(ind,understandingsratings,width)
		plt.axis([0,4.5,0,0.8])
		plt.xticks(ind+width/2.,('No Problems','Minor Problems','Major Problems','Session Stopped'))
		plt.title('Survey Q4: Understanding Your Partner')
		plt.ylabel('Proportion of Respondents')
		prob = badprobcalc(understandingsratings)
		plt.text(3.5,0.7,r'p$_{bad}$ = '+str(round(prob,3)))

		plt.subplot(325)
		plt.bar(ind,cuttingsratings,width)
		plt.axis([0,4.5,0,0.8])
		plt.xticks(ind+width/2.,('No Problems','Minor Problems','Major Problems','Session Stopped'))
		plt.title('Survey Q5: Sound Cutting In and Out')
		plt.ylabel('Proportion of Respondents')
		prob = badprobcalc(cuttingsratings)
		plt.text(3.5,0.7,r'p$_{bad}$ = '+str(round(prob,3)))

		plt.subplot(326)
		plt.bar(ind,whiteboardratings,width,color = 'orange')
		plt.axis([0,4.5,0,0.8])
		plt.xticks(ind+width/2.,('No Problems','Minor Problems','Major Problems','Session Stopped'))
		plt.title('Survey Q6: Whiteboard Functionality')
		plt.ylabel('Proportion of Respondents')
		prob = badprobcalc(whiteboardratings)
		plt.text(3.5,0.7,r'p$_{bad}$ = '+str(round(prob,3)))

		plt.suptitle('Aggregate Survey Results - '+self.school+'    N = '+str(length), fontsize=20)

		fig.set_size_inches(18.5,10.5)

		fig.savefig('Aggregate_Surveys_'+self.school)
		fig.clf()

		plt.close()

		return

class ACFullSurveyData():

	def __init__(self, dates, usernames, usertypes, locations, videos, browsers, operatingsystems, versions, overalls, hearing, delays, understandings, cuttings, videoprobs, whiteboardprobs):

		#  Link data to the object.
		self.dates = dates
		self.usernames = usernames
		self.usertypes = usertypes
		self.locations = locations
		self.videos = videos
		self.browsers = browsers
		self.operatingsystems = operatingsystems
		self.versions = versions
		self.overalls = overalls
		self.hearing = hearing
		self.delays = delays
		self.understandings = understandings
		self.cuttings = cuttings
		self.videoprobs = videoprobs
		self.whiteboardprobs = whiteboardprobs

	def aggregateSurvey(self):

		length = len(self.overalls)
		overallist = list()
		hearinglist = list()
		delayslist = list()
		understandingslist = list()
		cuttingslist = list()
		whiteboardlist = list()
		i = 0

		while (i < length):
			if (self.overalls[i] != ''):
				overallist.append(self.overalls[i])
			if (self.hearing[i] != ''):
				hearinglist.append(self.hearing[i])
			if (self.delays[i] != ''):
				delayslist.append(self.delays[i])
			if (self.understandings[i] != ''):
				understandingslist.append(self.understandings[i])
			if (self.cuttings[i] != ''):
				cuttingslist.append(self.cuttings[i])
			if (self.whiteboardprobs[i] != ''):
				whiteboardlist.append(self.whiteboardprobs[i])

			i += 1

		overalltab = np.array(overallCount(overallist))
		overallratings = overalltab/length

		hearingratings = np.array(problemCount(hearinglist))
		delaysratings = np.array(problemCount(delayslist))
		understandingsratings = np.array(problemCount(understandingslist))
		cuttingsratings = np.array(problemCount(cuttingslist))
		whiteboardratings = np.array(problemCount(whiteboardlist))

		fig = plt.figure()

		plt.subplot(321)
		ind = np.array([0.5,1.5,2.5,3.5])
		width = 0.65
		plt.bar(ind,overallratings, width,color='green')
		plt.axis([0,4.5,0,0.7])
		plt.xticks(ind+width/2.,('Excellent','Good','Fair','Poor'))
		plt.title('Survey Q1: Overall Experience')
		plt.ylabel('Proportion of Respondents')
		prob = badprobcalc(overallratings)
		plt.text(3.5,0.6,r'p$_{bad}$ = '+str(round(prob,3)))

		plt.subplot(322)
		plt.bar(ind,hearingratings,width,color = 'blue')
		plt.axis([0,4.5,0,0.7])
		plt.xticks(ind+width/2.,('No Problems','Minor Problems','Major Problems','Session Stopped'))
		plt.title('Survey Q2: Hearing Your Partner')
		plt.ylabel('Proportion of Respondents')
		prob = badprobcalc(hearingratings)
		plt.text(3.5,0.6,r'p$_{bad}$ = '+str(round(prob,3)))


		plt.subplot(323)
		plt.bar(ind,delaysratings,width)
		plt.axis([0,4.5,0,0.7])
		plt.xticks(ind+width/2.,('No Problems','Minor Problems','Major Problems','Session Stopped'))
		plt.title('Survey Q3: Delays in Audio')
		plt.ylabel('Proportion of Respondents')
		prob = badprobcalc(delaysratings)
		plt.text(3.5,0.6,r'p$_{bad}$ = '+str(round(prob,3)))

		plt.subplot(324)
		plt.bar(ind,understandingsratings,width)
		plt.axis([0,4.5,0,0.7])
		plt.xticks(ind+width/2.,('No Problems','Minor Problems','Major Problems','Session Stopped'))
		plt.title('Survey Q4: Understanding Your Partner')
		plt.ylabel('Proportion of Respondents')
		prob = badprobcalc(understandingsratings)
		plt.text(3.5,0.6,r'p$_{bad}$ = '+str(round(prob,3)))

		plt.subplot(325)
		plt.bar(ind,cuttingsratings,width)
		plt.axis([0,4.5,0,0.7])
		plt.xticks(ind+width/2.,('No Problems','Minor Problems','Major Problems','Session Stopped'))
		plt.title('Survey Q5: Sound Cutting In and Out')
		plt.ylabel('Proportion of Respondents')
		prob = badprobcalc(cuttingsratings)
		plt.text(3.5,0.6,r'p$_{bad}$ = '+str(round(prob,3)))

		plt.subplot(326)
		plt.bar(ind,whiteboardratings,width,color = 'orange')
		plt.axis([0,4.5,0,0.7])
		plt.xticks(ind+width/2.,('No Problems','Minor Problems','Major Problems','Session Stopped'))
		plt.title('Survey Q6: Whiteboard Functionality')
		plt.ylabel('Proportion of Respondents')
		prob = badprobcalc(whiteboardratings)
		plt.text(3.5,0.6,r'p$_{bad}$ = '+str(round(prob,3)))


		plt.suptitle('Adobe Connect - Aggregate Survey Results', fontsize=20)

		fig.set_size_inches(18.5,10.5)

		fig.savefig('AC_Aggregate_Surveys')
		fig.clf()

		plt.close()
		return
