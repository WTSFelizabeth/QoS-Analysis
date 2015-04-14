import datetime as dt

#  List of blackbox locations.
blackboxlocationlist = ['IBL_Thurs 9:50','IBL_Thurs 10:40','IBL_Thurs 11:30','IBL_Thurs 2:20','Sierramont Tue 10','Sierramont Tue 12',
'SLHS Thurs 12','SLHS Thurs 1','Testing']

#  Dictionary of blackbox start and end dates
blackboxstartandendforgraph = {'IBL':[dt.datetime(2015,3,29),dt.datetime(2015,4,4)],'Sierramont':[dt.datetime(2015,3,19),dt.datetime(2015,4,1)],
'SLHS':[dt.datetime(2015,3,19),dt.datetime(2015,4,2)],'Testing':[dt.datetime(2015,3,18),dt.datetime(2015,3,25)]}

#  Convert blackbox file name to locaiton list for that site.
blackboxlocationconvert = {'pilot-ibl':['IBL_Thurs 9:50','IBL_Thurs 10:40','IBL_Thurs 11:30','IBL_Thurs 2:20'],
'pilot-sierramont':['Sierramont Tue 10','Sierramont Tue 12'],'pilot-slhs':['SLHS Thurs 12','SLHS Thurs 1'],'testbox':['Testing']}

#  List of blackbox schools.
blackboxschoollist = ['IBL','Sierramont','SLHS','Testing']

#  List of session days at blackbox schools.
blackboxschooltoday = {'IBL':'Thu','Sierramont':'Tue','SLHS':'Thu','Testing':'Mon'}

#  Blackbox days to leave out of analysis (i.e. spring break, etc).
blackboxdaysout = {'IBL':[dt.datetime(2015,4,6),dt.datetime(2015,4,7),dt.datetime(2015,4,8),dt.datetime(2015,4,9),dt.datetime(2015,4,10)],
'Sierramont':[],'SLHS':[],'Testing':[]}