import sys
sys.path.append('C:/Python27x86/lib/site-packages')
import gclib

def main():

  g = gclib.py() #make an instance of the gclib python class
  
  try:
    
    #connect to network
    g.GOpen('10.1.2.245 --direct -s ALL')
    #print('gclib version:', g.GVersion())
    #g.GOpen('COM1 --direct')
    #print(g.GInfo())

    #used for galil commands
    c = g.GCommand
    
    c('AB') #abort motion and program
    c('MO') #turn off all motors
    c('SH') #servo on
    
    # deg to ct conversion for each motor
    degtoctsAZ = 1024000/360
    degtoctsE = 4096/360
    
    #azimuth scan settings
    time = 5 # move for 2 seconds
    azSP = 90 * degtoctsAZ # 90 deg/sec
    azD = 2*360 * degtoctsAZ #azSP * time

    #elevation settings
    elevSP = 180 * degtoctsE # x degrees/sec
    elevD = 10 * degtoctsE # move elevation x degrees each iteration

    iterations = 2 # how many iterations do you want to do

    #initial position
    P1AZ = (float(c('TPX')) % 1024000) / degtoctsAZ
    P1AZ = (float(c('TPX')) % 1024000) / degtoctsAZ
    P1E = (float(c('TPY')) % 4096) / degtoctsE
    print('AZ:', P1AZ, 'Elev:', P1E)

    #while count < iterations:
    for i in range(0,iterations):

      #gclib/galil commands to move elevation axis motor
      c('SPA=' + str(azSP)) #speed, cts/sec
      c('PRA=' + str(azD)) #relative move, 1024000 cts = 360 degrees
      print(' Starting iteration: ' + str(i + 1))
      c('BGA') #begin motion
      c('AMA') #wait for motion to complete
      #g.GMotionComplete('A')
      print(' done.')

      #change elevation for next az scan
      if i < iterations - 1:
        c('SPB=' + str(elevSP)) #elevation speed
        c('PRB=' + str(elevD)) # change the elevation by x deg
        c('BGB')
        c('AMB')

      P2AZ = (float(c('TPX')) % 1024000) / degtoctsAZ
      P2E = (float(c('TPY')) % 4096) / degtoctsE
      print('AZ:', P2AZ, 'Elev:', P2E)
    
    del c #delete the alias

  ###########################################################################
  # except handler
  ###########################################################################  
  except gclib.GclibError as e:
    print('Unexpected GclibError:', e)
  
  finally:
    g.GClose() #don't forget to close connections!
  
  return
  
 
#runs main() if example.py called from the console
if __name__ == '__main__':
  main()
  