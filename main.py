#  main.py
#  Created By:  Elizabeth Otto
#  Property Of: We Teach Science Foundation
#  Date Created:  10.13.14
#  Last Modified: 10.13.14
#  Description:  

import numpy as np
import scipy as sp
import matplotlib as mpl
import csv
import datetime as dt

from pingdata import PingData
from surveydata import ClassSurveyData

from pinganalysis import *
from surveyanalysis import *
from sessionanalysis import *

from pingfilelist import *
from testboxfilelist import *


#import all the ping data (required:  list of files)
pinglist = pingimport(pingfiles)
blackboxpinglist = blackboximport(blackboxpingfiles)

#import the surveys
classsurveylist = surveycontroller('surveys.txt')

#  Feed the survey and class ping data to the session analysis module.
sessionanalysis(classsurveylist,pinglist)