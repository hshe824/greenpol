import scan
import scantest
import sys
sys.path.append('C:/Python27x86/lib/site-packages')
import gclib
import moveto


#make an instance of the gclib python class
g = gclib.py()
#connect to network
g.GOpen('10.1.2.245 --direct -s ALL')
#
#g.GOpen('COM1 --direct')
#used for galil commands
c = g.GCommand

c('AB') #abort motion and program
c('MO') #turn off all motors
c('SH') #servo on

#how long should it scan in azimuth before switching elevations, in seconds
tscan = 5
#numRotations = 1

# how many different elevations to scan at
iterations = 2

#difference in elevation for each scan
deltaEl = 90.

#starting elevation and azimuth
az0 = 60.
el0 = 0.

moveto.location(az0, el0, c) 
scan.azScan(tscan, iterations,  deltaEl, c)
#scantest.azScan(numRotations, iterations, deltaEl, c)

g.GClose() #close connections