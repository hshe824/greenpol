# move from some initial position to a final position

import planets
import config
import sys
sys.path.append('C:/Python27x86/lib/site-packages')
sys.path.append('D:/software_git_repos/greenpol/telescope_control/data_aquisition')
import gclib
import get_pointing as gp

'''
def wait(c):
    while int(float(c('MG _BGA'))) == 1 or int(float(c('MG _BGB'))) == 1:
        pass
'''
def wait(c):
    while c('MG _BGA') != '0.0000' or c('MG _BGB') != '0.0000':
        #print(c('MG _BGA'),c('MG _BGB'))

        pass


def location(az, el, c):
  #g = gclib.py() #make an instance of the gclib python class
  
  try:
    

    #print('gclib version:', g.GVersion())
    #g.GOpen('COM1 --direct')
    #print(g.GInfo())

    c = c

    ######################################

    # deg to ct conversion for each motor
    degtoctsAZ = config.degtoctsAZ
    degtoctsEl = config.degtoctsEl 

    #offset between galil and beam
    offsetAz = gp.galilAzOffset 
    offsetEl = gp.galilElOffset 

    #where you are currently
    P1AZ = (float(c('TPX'))+offsetAz*degtoctsAZ) % (degtoctsAZ * 360.) 
    #P1AZ = P1AZ - offset, or replace TP
    P1El = (float(c('TPY'))+offsetEl*degtoctsEl) % (degtoctsEl * 360.) 
    print('AZ_0:', P1AZ / degtoctsAZ, 'Elev_0:', P1El / degtoctsEl)


    #keep telescope from pointing below horizon
    if el < 0. or el > 180.:
        print('Warning, this elevation is below the horizon, your going to break the telescope...')
        return 

    #convert new coordinates to cts
    P2AZ = az % 360 * degtoctsAZ
    P2El = el % 360 * degtoctsEl
    
    #azimuth scan settings
    azSP = config.azSPm # speed
    azAC = config.azAC # acceleration 
    azDC = config.azDC # deceleration

    azD = (P2AZ - P1AZ) # distance to desired az
    
    #make it rotate the short way round
    if azD > 180. * degtoctsAZ:
        azD = azD - 360.*degtoctsAZ

    if azD < -180. * degtoctsAZ:
        azD = 360. * degtoctsAZ + azD

    
    #elevation settings
    elevSP = config.elevSP # x degrees/sec
    elevAC = config.elevAC # acceleration 
    elevDC = config.elevDC # deceleration

    elevD = (P2El - P1El) # distance to desired elev

    '''    
    #make it rotate the short way round, this might be unecessary for el
    if elevD > 180. * degtoctsEl:
        elevD = elevD - 360. * degtoctsEl
    
    if elevD < -180. * degtoctsEl:
        elevD = 360. * degtoctsEl + elevD
    '''

    #gclib/galil commands to move az motor
    c('SPA=' + str(azSP)) #speed, cts/sec
    c('ACA=' + str(azAC)) #speed, cts/sec
    c('DCA=' + str(azDC)) #speed, cts/sec
    c('PRA=' + str(azD)) #relative move

    #gclib/galil commands to move elevation motor
    c('SPB=' + str(elevSP)) #elevation speed
    c('ACB=' + str(elevAC)) #speed, cts/sec
    c('DCB=' + str(elevDC)) #speed, cts/sec
    c('PRB=' + str(elevD)) #relative move

    print('Moving to object location')
    c('BGA') #begin motion 
    #g.GMotionComplete('A')
    wait(c)
    if c('MG _SCA') != '1.0000':
        return

    c('BGB') # begin motion

    #wait for both az and el motors to finish moving
    #c('AMB')
    #c('AMA')
    wait(c)

    #if it hasnt reached its intended position, 
    #its because I stopped it and the function should end
    if c('MG _SCB') != '1.0000':
        return
    #g.GMotionComplete('A')
    #g.GMotionComplete('B')
    print(' done.')

    #final position
    AZ_f = ((float(c('TPX')) / degtoctsAZ) + offsetAz) % 360. 
    Elev_f = ((float(c('TPY')) / degtoctsEl) + offsetEl) % 360.  
    print('AZ_f:', AZ_f, 'Elev_f:', Elev_f)
 
    del c #delete the alias

  ###########################################################################
  # except handler
  ###########################################################################  
  except gclib.GclibError as e:
    print('Unexpected GclibError:', e)
  
  return

def distance(az, el, c):
  #g = gclib.py() #make an instance of the gclib python class
  
  try:
    print('Moving now...')

    #print('gclib version:', g.GVersion())
    #g.GOpen('COM1 --direct')
    #print(g.GInfo())

    c = c

    ######################################

    # deg to ct conversion for each motor
    degtoctsAZ = config.degtoctsAZ
    degtoctsEl = config.degtoctsEl

    #offset between galil and beam
    offsetAz = gp.galilAzOffset 
    offsetEl = gp.galilElOffset 

    #where you are currently
    P1AZ = float(c('TPX'))
    P1El = float(c('TPY')) 
    AZ_0 = ((P1AZ / degtoctsAZ) + offsetAz) % 360.
    Elev_0 = ((P1El / degtoctsEl) + offsetEl) % 360.
    print('AZ_0:', AZ_0, 'Elev_0:', Elev_0)


    #keep telescope from pointing below horizon
    if ((Elev_0 + el) % 360.) < 0. or ((Elev_0 + el) % 360.) > 180.:
        print Elev_0, el, Elev_0 + el
        print('Warning, this elevation is below the horizon, your going to break the telescope...')
        return 
    
    
    #make it rotate the short way round + keep it between 0 and 180
    if el > 180.:
        el = el - 360.
        print('Rotating to the same spot but making sure you dont go below horizon')
    
    if el < -180.:
        el = 360. + el
        print('Rotating to the same spot but making sure you dont go below horizon')
     
    #convert distance coordinates to cts
    P2AZ = az  * degtoctsAZ
    P2El = el  * degtoctsEl

    #azimuth scan settings
    azSP = config.azSPm # 90 deg/sec
    azAC = config.azAC # acceleration 
    azDC = config.azDC # deceleration

    azD = P2AZ # distance to desired az
    
    #elevation settings
    elevSP = config.elevSP # x degrees/sec
    elevAC = config.elevAC # acceleration 
    elevDC = config.elevDC # deceleration

    elevD = P2El # distance to move elev by
    
    #gclib/galil commands to move az motor
    c('SPA=' + str(azSP)) #speed, cts/sec
    c('ACA=' + str(azAC)) #speed, cts/sec
    c('DCA=' + str(azDC)) #speed, cts/sec
    c('PRA=' + str(azD)) #relative move

    #gclib/galil commands to move elevation motor
    c('SPB=' + str(elevSP)) #elevation speed
    c('ACB=' + str(elevAC)) #speed, cts/sec
    c('DCB=' + str(elevDC)) #speed, cts/sec
    c('PRB=' + str(elevD)) #relative move

    print(' Starting Motion...')

    c('BGA') #begin motion 
    #g.GMotionComplete('A')
    wait(c)

    #if it hasnt reached its intended position, 
    #its because I stopped it and the function should end
    if c('MG _SCA') != '1.0000':
        return

    c('BGB') # begin motion

    #wait for both az and el motors to finish moving
    wait(c)

    #if it hasnt reached its intended position, 
    #its because I stopped it and the function should end
    if c('MG _SCB') != '1.0000':
        return
    #c('AMA')
    #c('AMB')
    #g.GMotionComplete('A')
    #g.GMotionComplete('B')
    print(' done.')

    #final position
    AZ_f = ((float(c('TPX')) / degtoctsAZ)+offsetAz) % 360. 
    Elev_f = ((float(c('TPY')) / degtoctsEl)+offsetEl) % 360.  
    print('AZ_f:', AZ_f, 'Elev_f:', Elev_f)
 
    del c #delete the alias

  ###########################################################################
  # except handler
  ###########################################################################  
  except gclib.GclibError as e:
    print('Unexpected GclibError:', e)
  
  return

  
'''
g = gclib.py()
g.GOpen('10.1.2.245 --direct -s ALL')
c = g.GCommand

az = 90
el = 0

#location(az, el, c)
distance(az, el, c)
'''