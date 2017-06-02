#script for linear and horizontal scan patterns

import config
import moveto
import planets
import sys
sys.path.append('C:/Python27x86/lib/site-packages')
import gclib
from datetime import datetime, timedelta


def azScan(numRotations, iterations, deltaEl, c):
 
  try:

    c = c
    
    # deg to ct conversion for each motor
    degtoctsAZ = config.degtoctsAZ
    degtoctsE = config.degtoctsE
    
    #azimuth scan settings
    azSP = config.azSP # az scan speed, 90 deg/sec
    azAC = config.azAC # acceleration 
    azDC = config.azDC # deceleration
    azD = numRotations * 360. * degtoctsAZ

    #gclib/galil commands to set az axis motor motion
    c('SPA=' + str(azSP)) #speed, cts/sec
    c('ACA=' + str(azAC)) #acceleration, cts/sec
    c('DCA=' + str(azDC)) #deceleration, cts/sec
    c('PRA=' + str(azD)) # change the az by x deg

    #elevation settings
    elevSP = config.elevSP # x degrees/sec
    elevAC = config.elevAC # acceleration 
    elevDC = config.elevDC # deceleration
    elevD = deltaEl * degtoctsE # move elevation x degrees each iteration

    #gclib/galil commands to set az axis motor motion
    c('SPB=' + str(elevSP)) #elevation speed
    c('ACB=' + str(elevAC)) #acceleration, cts/sec
    c('DCB=' + str(elevDC)) #deceleration, cts/sec
    c('PRB=' + str(elevD)) # change the elevation by x deg

    #initial position
    P1AZ = (float(c('TPX')) % 1024000) / degtoctsAZ
    P1E = (float(c('TPY')) % 4096) / degtoctsE
    print('AZ:', P1AZ, 'Elev:', P1E)

    #while count < iterations:
    for i in range(0, iterations):

      print(' Starting az Scan: ' + str(i + 1))

      c('BGA') #begin motion
      #c('ADA=' + str(azD))

      print(' done.')

      #final position after each az scan
      P2AZ = (float(c('TPX'))) % 1024000 / degtoctsAZ
      P2E = float(c('TPY')) % 4096 / degtoctsE
      print('AZ:', P2AZ, 'Elev:', P2E)

      #change elevation for next az scan
      if i < iterations - 1:
        print('changing elevation')

        c('BGB') #begin motion
        c('AMB') #wait for motion to complete
        print('done')
        

        #position after each elevation change
        P2AZ = (float(c('TPX'))) % 1024000 / degtoctsAZ
        P2E = float(c('TPY')) % 4096 / degtoctsE
        print('AZ:', P2AZ, 'Elev:', P2E)
    
    del c #delete the alias

  ###########################################################################
  # except handler
  ###########################################################################  
  except gclib.GclibError as e:
    print('Unexpected GclibError:', e)
    
  return
  