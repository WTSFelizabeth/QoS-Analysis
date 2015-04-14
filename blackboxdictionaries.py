#  List of blackbox locations.
blackboxlocationlist = ['IBL_Thurs 9:50','IBL_Thurs 10:40','IBL_Thurs 11:30','IBL_Thurs 2:20','Sierramont Tue 10','Sierramont Tue 12',
'SLHS Thurs 12','SLHS Thurs 1','Testing']

#  Convert blackbox file name to locaiton list for that site.
blackboxlocationconvert = {'pilot-ibl':['IBL_Thurs 9:50','IBL_Thurs 10:40','IBL_Thurs 11:30','IBL_Thurs 2:20'],
'pilot-sierramont':['Sierramont Tue 10','Sierramont Tue 12'],'pilot-slhs':['SLHS Thurs 12','SLHS Thurs 1'],'testbox':['Testing']}

#  List of blackbox schools.
blackboxschoollist = ['IBL','Sierramont','SLHS','Testing']

#  List of session days at blackbox schools.
blackboxschooltoday = {'IBL':'Thu','Sierramont':'Tue','SLHS':'Thu','Testing':'Mon'}

#  Blackbox days to leave out of analysis (i.e. spring break, etc).
blackboxdaysout = {'IBL':[],'Sierramont':[],'SLHS':[],'Testing':[]}