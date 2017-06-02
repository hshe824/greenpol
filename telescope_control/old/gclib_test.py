import gclib


def main():
  g = gclib.py() #make an instance of the gclib python class
  
  try:
    print('gclib version:', g.GVersion())

    ###########################################################################
    #  Connect
    ###########################################################################
    g.GOpen('10.1.2.245 --direct -s ALL')
    #g.GOpen('10.1.2.250 --direct -s ALL')
    #g.GOpen('COM1 --direct')
    print(g.GInfo())

    #Motion Complete

    c = g.GCommand
    
    #c('AB') #abort motion and program
    #c('MO') #turn off all motors
    #c('SH') #servo on
    
    # deg to ct conversion for each motor
    degtoctsA = 1024000/360
    degtoctsB = 4096/360
    
    #azimuth settings
    time = 2 # move for 2 seconds
    azSP = 90 * degtoctsA # 90 deg/sec
    azD = azSP * time

    #elevation settings
    elevSP = 180 * degtoctsB # x degrees/sec
    elevD = 90 * degtoctsB # move elevation x degrees

    count = 0
    iterations = 1 # how many iterations do you want to do
  
    print(c('TP'))

    while count < iterations:

      c('SPA=' + str(azSP)) #speed, cts/sec
      c('PRA=' + str(azD)) #relative move, 1024000 cts = 360 degrees
      print(' Starting iteration: ' + str(count + 1))
      c('BGA') #begin motion
      c('AMA')
      #g.GMotionComplete('A')
      print(' done.')

      if count < iterations - 1:
        c('SPB=' + str(elevSP)) #elevation speed
        c('PRB=' + str(elevD)) # change the elevation by x deg
        c('BGB')
        c('AMB')

      count += 1
    print 'hey'
    print(c('TP'))
    
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
  