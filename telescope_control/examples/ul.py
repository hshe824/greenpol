# example1.py
import UniversalLibrary as UL
import time

BoardNum = 0
Gain = UL.BIP5VOLTS
Chan = 0

tstart = time.time()
data = []
times = []
while 1:
    DataValue = UL.cbAIn(BoardNum, Chan, Gain)
    data.append( DataValue )
    times.append( time.time()-tstart )
    if times[-1] > 1.0:
        break

import pylab
pylab.plot(times,data,'o-')
pylab.xlabel('time (sec)')
pylab.ylabel('ADC units')
pylab.show()