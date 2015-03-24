#  dictionaries.py
#  Dictionaries and lists for use within analysis suite.

#  Months of the year converted to numerical form.
months = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}

#  Days of week converted to numerical form.
daystonum = {'Mon':0,'Tue':1,'Wed':2,'Thu':3,'Fri':4,'Sat':5,'Sun':6}

#  Numerical form of day of week converted to name.
numtodays = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}

#  Convert from class name to the name fo the school.
classtoschool = {'Cabrillo':'Cabrillo','Castlemont Tue 9:40':'Castlemont','Castlemont Tue 11:50':'Castlemont','Columbia':'Columbia','IBL_Thurs 9:50':'IBL',
'IBL_Thurs 10:40':'IBL','IBL_Thurs 11:30':'IBL','IBL_Thurs 2:20':'IBL','Horn':'Horn','Irving High Thurs 1':'Irving','Irving High Thurs 9':'Irving',
'Irving High Thurs 3':'Irving','Morrill':'Morrill','Nimitz Wed 12':'Nimitz','Nimitz Wed 10':'Nimitz',
'Nimitz Wed 3':'Nimitz', 'Overfelt':'Overfelt', 'Piedmont':'Piedmont','RL Turner Tue 8':'RL Turner','RL Turner Tue 1':'RL Turner',
'Sierramont Tue 10':'Sierramont','Sierramont Tue 12':'Sierramont','SLHS Thurs 12':'SLHS','SLHS Thurs 1':'SLHS','SLHS Thurs 2':'SLHS',
'Testing':'Testing'}

#  List of participating classes.
classlist = ['Cabrillo','Castlemont Tue 9:40','Castlemont Tue 11:50','Columbia','IBL_Thurs 9:50','IBL_Thurs 10:40','IBL_Thurs 11:30','IBL_Thurs 2:20',
'Horn','Irving High Thurs 1', 'Irving High Thurs 9','Irving High Thurs 3','Morrill','Nimitz Wed 12', 'Nimitz Wed 10', 'Nimitz Wed 3', 
'Overfelt', 'Piedmont', 'RL Turner Tue 8','RL Turner Tue 1','Sierramont Tue 10', 'Sierramont Tue 12','SLHS Thurs 12', 'SLHS Thurs 1', 
'SLHS Thurs 2','Testing']

#  Convert class names to single format.
classformatconvert = {'IBL_Thurs 9:50':'IBL_Thurs 9_50','IBL_Thurs 10:40':'IBL_Thurs 10_40','IBL_Thurs 11:30':'IBL_Thurs 11_30',
'IBL_Thurs 2:20':'IBL_Thurs 2_20','Cabrillo':'Cabrillo','Castlemont Tue 9:40':'Castlemont Tue 9:40','Castlemont Tue 11:50':'Castlemont Tue 11:50',
'Columbia':'Columbia','Horn':'Horn','Irving High Thurs 1':'Irving High Thurs 1','Irving High Thurs 9':'Irving High Thurs 9',
'Irving High Thurs 3':'Irving High Thurs 3','Morrill':'Morrill','Nimitz Wed 12':'Nimitz Wed 12','Nimitz Wed 10':'Nimitz Wed 10',
'Nimitz Wed 3':'Nimitz Wed 3','Overfelt':'Overfelt','Piedmont':'Piedmont','RL Turner Tue 8':'RL Turner Tue 8','RL Turner Tue 1':'RL Turner Tue 1',
'Sierramont Tue 10':'Sierramont Tue 10','Sierramont Tue 12':'Sierramont Tue 12','SLHS Thurs 12':'SLHS Thurs 12','SLHS Thurs 1':'SLHS Thurs 1',
'SLHS Thurs 2':'SLHS Thurs 2','Testing':'Testing'}

#  Enrollment in each class.
classenrollment = {'Castlemont Tue 9:40':5,'Castemont Tue 11:50':2,'Columbia':8,'IBL_Thurs 9:50':19,'IBL_Thurs 10:40':27,'IBL_Thurs 11:30':20,
'IBL_Thurs 2:20':11,'Irving High Thurs 9':13,'Irving High Thurs 3':13,'Morrill':12,'Nimitz Wed 10':16,'Nimitz Wed 12':21,'Nimitz Wed 3':18,
'Overfelt':19,'Piedmont':15,'RL Turner Tue 8':13,'RL Turner Tue 1':15,'SLHS Thurs 12':14,'SLHS Thurs 1':14,'SLHS Thurs 2':21,
'Sierramont Tue 10':17,'Sierramont Tue 12':19}

# Find day of week based on the class.
classtoday = {'Cabrillo':'Mon','Castlemont Tue 9:40':'Tue','Castlemont Tue 11:50':'Tue','Columbia':'Wed','IBL_Thurs 9:50':'Thu',
'IBL_Thurs 10:40':'Thu','IBL_Thurs 11:30','Thu','IBL_Thurs 2:20':'Thu','Horn':'Mon','Irving High Thurs 1':'Thu', 'Irving High Thurs 9':'Thu',
'Irving High Thurs 3':'Thu','Morrill':'Tue','Nimitz Wed 12':'Wed', 'Nimitz Wed 10':'Wed', 'Nimitz Wed 3':'Wed', 'Overfelt':'Thu', 
'Piedmont':'Tue', 'RL Turner Tue 8','Tue','RL Turner Tue 1':'Tue','Sierramont Tue 10':'Tue', 'Sierramont Tue 12','Tue','SLHS Thurs 12':'Thu',
'SLHS Thurs 1':'Thu', 'SLHS Thurs 2','Thu','Testing':'Mon'}

#  Find session start and end time based on class.

# Student operating system in each class.
classtostudentos = {'Cabrillo':'Testing','Castlemont Tue 9:40':'Windows','Castlemont Tue 11:50':'Windows','Columbia':'Columbia',
'Horn':'Testing','IBL_Thurs 9:50':'Windows','IBL_Thurs 10:40':'Windows','IBL_Thurs 11:30':'Windows','IBL_Thurs 2:20':'Windows',
'Irving High Thurs 1':'Windows','Irving High Thurs 9':'Windows','Irving High Thurs 3':'Windows','Morrill':'OS X',
'Nimitz Wed 12':'Windows','Nimitz Wed 10':'Windows','Nimitz Wed 3':'Windows','Overfelt':'Windows','Piedmont':'Chromebook',
'RL Turner Tue 8':'Windows','RL Turner Tue 1':'Windows','Sierramont Tue 10':'Chromebook','Sierramont Tue 12':'Chromebook',
'SLHS Thurs 12':'Windows','SLHS Thurs 1':'Windows','SLHS Thurs 2':'OS X','Testing':'Testing'}

#  Type of network in each class.
classtonetwork = {'Cabrillo':'Testing','Castlemont Tue 9:40':'wired','Castlemont Tue 11:50':'wired','Columbia':'wired',
'Horn':'Testing','IBL_Thurs 9:50':'wired','IBL_Thurs 10:40':'wired','IBL_Thurs 11:30':'wired','IBL_Thurs 2:20':'wired',
'Irving High Thurs 1':'wireless','Irving High Thurs 9':'wireless','Irving High Thurs 3':'wireles','Morrill':'wired',
'Nimitz Wed 12':'wireless','Nimitz Wed 10':'wireless','Nimitz Wed 3':'wireless','Overfelt':'wired','Piedmont':'wireless',
'RL Turner Tue 8':'wired','RL Turner Tue 1':'wired','Sierramont Tue 10':'wireless','Sierramont Tue 12':'wireless',
'SLHS Thurs 12':'wired','SLHS Thurs 1':'wired','SLHS Thurs 2':'wired','Testing':'Testing'}

#  Day of 

#  List of schools.
schoollist = ['Cabrillo','Castlemont','Columbia','IBL','Horn','Irving','Morrill','Nimitz','Overfelt','Piedmont','RL Turner','Sierramont','SLHS','Testing']

#  Overall ratings for technology and conversion to numerical scale.
overallratings = {'Excellent':4,'Good':3,'Fair':2,'Poor':1}

#  Ratings for each problem and conversion to numerical scale.
propertyratings = {'none':4,'small':3,'large':2,'worst':1}

#  List of operating systems.
oslist = ['Windows','OS X','Chromebook']