import datetime as dt

#  List of blackbox locations.
blackboxlocationlist = ['IBL_Thurs 9:50','IBL_Thurs 10:40','IBL_Thurs 11:30','IBL_Thurs 2:20','Sierramont Tue 10','Sierramont Tue 12',
'SLHS Thurs 12','SLHS Thurs 1','Testing']

#  Dictionary of blackbox start and end dates
blackboxstartandendforgraph = {'IBL':[dt.datetime(2015,3,29),dt.datetime(2015,4,4)],'Sierramont':[dt.datetime(2015,4,1),dt.datetime(2015,4,22)],
'SLHS':[dt.datetime(2015,4,1),dt.datetime(2015,4,22)],'Testing':[dt.datetime(2015,3,18),dt.datetime(2015,3,25)]}

blackboxstartandendforanalysis = {'IBL':[dt.datetime(2015,3,27),dt.datetime(2015,4,23)],'Sierramont':[dt.datetime(2015,3,19),dt.datetime(2015,4,23)],
'SLHS':[dt.datetime(2015,3,21),dt.datetime(2015,4,23)],'Testing':[dt.datetime(2015,3,18),dt.datetime(2015,3,25)]}

#  Convert blackbox file name to location list for that site.
blackboxlocationconvert = {'pilot-ibl':['IBL_Thurs 9:50','IBL_Thurs 10:40','IBL_Thurs 11:30','IBL_Thurs 2:20'],
'pilot-sierramont':['Sierramont Tue 10','Sierramont Tue 12'],'pilot-slhs':['SLHS Thurs 12','SLHS Thurs 1'],'testbox':['Testing']}

#  List of blackbox schools.
blackboxschoollist = ['IBL','Sierramont','SLHS','Testing']

#  List of session days at blackbox schools.
blackboxschooltoday = {'IBL':'Thu','Sierramont':'Tue','SLHS':'Thu','Testing':'Mon'}

#  Blackbox days to leave out of analysis (i.e. spring break, etc).
blackboxdaysout = {'IBL':[dt.datetime(2015,3,25),dt.datetime(2015,3,26),dt.datetime(2015,4,6),dt.datetime(2015,4,7),dt.datetime(2015,4,8),
dt.datetime(2015,4,9),dt.datetime(2015,4,10),dt.datetime(2015,4,16),dt.datetime(2015,4,21)],'Sierramont':[dt.datetime(2015,3,16),
dt.datetime(2015,3,17),dt.datetime(2015,3,18),dt.datetime(2015,4,2),dt.datetime(2015,4,13),
dt.datetime(2015,4,14),dt.datetime(2015,4,15),dt.datetime(2015,4,16),dt.datetime(2015,4,21)],
'SLHS':[dt.datetime(2015,3,16),dt.datetime(2015,3,17),dt.datetime(2015,3,19),dt.datetime(2015,4,3),
dt.datetime(2015,4,13),dt.datetime(2015,4,16),dt.datetime(2015,4,21)],'Testing':[]}

#  Special exceptions
blackboxspecial = {'IBL':False,'Sierramont':True,'SLHS':False,'Testing':False}

#  Blackbox days to move to non-session days.
blackboxdaysnosession = {'IBL_Thurs 9:50':[],'IBL_Thurs 10:40':[],'IBL_Thurs 11:30':[],'IBL_Thurs 2:20':[],
'Sierramont Tue 10':[dt.datetime(2015,3,24),dt.datetime(2015,3,31),dt.datetime(2015,4,21),dt.datetime(2015,4,28)],
'Sierramont Tue 12':[dt.datetime(2015,3,24),dt.datetime(2015,3,31),dt.datetime(2015,4,21),dt.datetime(2015,4,28)],
'SLHS Thurs 12':[],'SLHS Thurs 1':[],'Testing':[]}

#  Blackbox days that are session days.
blackboxdayssessions = {'IBL_Thurs 9:50':[],'IBL_Thurs 10:40':[],'IBL_Thurs 11:30':[],'IBL_Thurs 2:20':[],
'Sierramont Tue 10':[dt.datetime(2015,3,23),dt.datetime(2015,3,30),dt.datetime(2015,4,20),dt.datetime(2015,4,27)],
'Sierramont Tue 12':[dt.datetime(2015,3,23),dt.datetime(2015,3,30),dt.datetime(2015,4,20),dt.datetime(2015,4,27)],
'SLHS Thurs 12':[],'SLHS Thurs 1':[],'Testing':[]}

#  Special start times.
blackboxspecialtimesstart = {'Sierramont Tue 10':dt.time(13,35,0),'Sierramont Tue 12':dt.time(11,8,0)}

#  Special end times.
blackboxspecialtimesend = {'Sierramont Tue 10':dt.time(14,30,0),'Sierramont Tue 12':dt.time(12,3,0)}



