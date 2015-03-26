#  pingdata.py
#  Created By:  Elizabeth Otto
#  Property Of: We Teach Science Foundation
#  Date Created:  10.13.14
#  Last Modified: 10.20.14
#  Description:  

import numpy as np
import scipy as sp
import datetime as dt
import matplotlib as mpl
import matplotlib.pyplot as plt

#  Class for PingData objects.
class PingData:

	logcount = 0

	#  Create a PingData object.
	def __init__(self, location, date, bandwidth, times, pingtimes, jitters):

		#  Link data to the object.
		self.location = location
		self.date = date
		self.bandwidth = bandwidth
		self.times = times
		self.pingtimes = pingtimes
		self.jitters = jitters

		#  Increment count.
		PingData.logcount += 1

	#  Calculate the average ping time within a single PingData object.
	def averagePing(self):
		meanping = np.mean(self.pingtimes)
		return meanping

	#  Calculate the average jitter within a single PingData object.
	def averageJitter(self):
		meanjitter = np.mean(self.jitters)
		return meanjitter

	#  Create a diagnostic plot of the ping times from the PingData object.
	def plotPings(self):

		fig = plt.figure()
		plt.plot(self.times,self.pingtimes)
		plt.gca().xaxis.set_major_formatter(mpl.dates.DateFormatter("%H:%M"))
		plt.title(self.location + ' ' + dt.date.__str__(self.date))
		plt.xlabel('Time')
		plt.ylabel('Ping Time (ms)')

		fig.savefig('Ping_'+self.location+'_'+dt.date.__str__(self.date))
		fig.clf

		return

	#  Create a diagnostic plot of the jitters from the PingData object.
	def plotJitters(self):

		fig = plt.figure()
		plt.plot(self.times,self.jitters)
		plt.gca().xaxis.set_major_formatter(mpl.dates.DateFormatter("%H:%M"))
		plt.title(self.location + ' ' + dt.date.__str__(self.date))
		plt.xlabel('Time')
		plt.ylabel('Jitter (ms)')

		fig.savefig('Jitter_'+self.location+'_'+dt.date.__str__(self.date))
		fig.clf

		return

#  Class for blackbox objects.
class BlackboxData:

		#  Create a PingData object.
	def __init__(self, location, date, dayofweek, times, pingtimes, jitters, losses,session):

		#  Link data to the object.
		self.location = location
		self.dayofweek = dayofweek
		self.date = date
		self.times = times
		self.pingtimes = pingtimes
		self.jitters = jitters
		self.losses = losses

		#  Create flag to determine whether this data contains a session day.
		self.session = session
