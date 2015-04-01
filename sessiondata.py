#  sessiondata.py
#  Created By:  Elizabeth Otto
#  Property Of: We Teach Science Foundation
#  Date Created:  12.7.14
#  Last Modified: 12.7.14
#  Description:

from __future__ import division

import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
import csv
import datetime as dt
import pylab

from dictionaries import classenrollment

def problemaverage(list,number):

	number = float(number)

	total = 0
	total += list[0]*4.*number
	total += list[1]*3.*number
	total += list[2]*2.*number
	total += list[3]*1.*number

	metric = total/number

	return metric

class SessionStats:

	def __init__(self, location, date, number, overallcount, hearingcount, delaycount, understandingcount, cuttingcount, videocount, whiteboardcount, pings, 
		jitters, bandwidth, bpings, bjitters, blosses):

		#  Link data to the object.
		self.location = location
		self.date = date
		self.number = number
		self.overallcount = overallcount
		self.hearingcount = hearingcount
		self.delaycount = delaycount
		self.understandingcount = understandingcount
		self.cuttingcount = cuttingcount
		self.videocount = videocount
		self.whiteboardcount = whiteboardcount
		self.pings = pings
		self.jitters = jitters
		self.bandwidth = bandwidth
		self.bpings = bpings
		self.bjitters = bjitters
		self.blosses = blosses

	def overallmetric(self):

		number = float(self.number)

		excellenttot = self.overallcount[0]*number*4.
		goodtot = self.overallcount[1]*number*3.
		fairtot = self.overallcount[2]*number*2.
		poortot = self.overallcount[3]*number*1.


		total = excellenttot + goodtot + fairtot + poortot

		metric = total/number

		return metric

	def problemmetrics(self):

		hearingmetric = problemaverage(self.hearingcount,self.number)
		delaymetric = problemaverage(self.delaycount,self.number)
		understandingmetric = problemaverage(self.understandingcount,self.number)
		cuttingmetric = problemaverage(self.cuttingcount,self.number)
		videometric = problemaverage(self.videocount,self.number)
		whiteboardmetric = problemaverage(self.whiteboardcount,self.number)

		return hearingmetric,delaymetric,understandingmetric,cuttingmetric,videometric,whiteboardmetric

	def averageping(self):

		average = sum(self.pings)/len(self.pings)

		return average

	def averagepingstdev(self):

		average = self.averageping()
		number = len(self.pings)
		total = 0

		for item in self.pings:
			total += (item-average)**2

		variance = (1/(number-1))*total
		stdev = variance**0.5
		stdevmean = stdev/(number**0.5)

		return stdevmean

	def maxminping(self):

		maximum = max(self.pings)
		minimum = min(self.pings)

		diff = maximum - minimum

		return diff

	def averagejitter(self):

		average = sum(self.jitters)/len(self.jitters)

		return average

	def completion(self):

		possiblesurveys = classenrollment[self.location]*2

		completionpercentage = round(100*float(self.number)/possiblesurveys,1)

		return completionpercentage

