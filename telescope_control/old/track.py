#script to track planets for telescope calibration

import moveto
import planets
import scan
import sys
sys.path.append('C:/Python27x86/lib/site-packages')
import gclib

#make an instance of the gclib python class
g = gclib.py()
#connect to network
g.GOpen('10.1.2.245 --direct -s ALL')
#used for galil commands
c = g.GCommand

c('AB') #abort motion and program
c('MO') #turn off all motors
c('SH') #servo on

location = "UCSB" #observation location
cbody = "Sun" # celestial body of observation

#+/- azimuth for each back and forth scan
MinAz = -10
MaxAz = 10

#min and max elevation for horizontal scan
MinEl = -10
MaxEl = 10

#delta elevation for each step in horizontal scan
stepSize = 10.

#number of back and forth azimuth scans at each elevation
numAzScans = 2

#do a linear scan at a fixed elevation
#scan.linearScan(location, cbody, numAzScans, MinAz, MaxAz, c)

#do a horizontal scan at x elevations
scan.horizontalScan(location, cbody, numAzScans, MinAz, MaxAz, MinEl, MaxEl, stepSize, c)


g.GClose() #close connections
