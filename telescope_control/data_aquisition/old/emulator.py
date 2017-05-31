import random, time, cPickle
import serial, serial.tools.list_ports

### PARAMETERS ###
STDFREQ = 1/(120.e-6) #Number of packets per second
PCKTSIZE = 50 #Number of bytes per packet
STDNAME = 'COM2' # Portname used for serial port
NPACKETS = 1e6 #Number of packets to send

# NOTES:
# This emulator saves the sent packet data to testdata.dat with cPickle.
# This emulator WILL overwrite this .dat file with the latest test data
# each time.
# I had to install a COMPORT simulator on my computer, as you cannot create
# COMPorts, virtual or otherwise, in Python; you have to do that via a driver.
# This emulator requires that PySerial be installed.
# On a side note: Every 1000 (1e4) packets will take ~1.2 seconds to send.

def rnd_packet():
    '''
    #Returns a randomly generated info packet.
    plist = [0]
    i = 0
    while i < (PCKTSIZE-1):
        #plist.append(random.randint(1,255))
        plist.append(i)
        i += 1
    plist = tuple(plist)
    return plist
    '''
    plist = np.arange(0, PCKTSIZE).tolist()
    return plist




def main():
    print 'Ports: ' + `serial.tools.list_ports_windows.comports()` # Lists visible comports
    baudrate = STDFREQ*PCKTSIZE*8
    pname = STDNAME
    sport = serial.Serial(port = pname, baudrate=baudrate, timeout = 0, write_timeout=0) # Initializes port access
    chkfile = open('testdata.dat', 'w') # Sets up data file for sent packets
    npackets = NPACKETS # Number of packets to send to port.
    n = 0
    nbytes = 0
    time.clock()
    
    while n < npackets:
        pckt = rnd_packet()
        cPickle.dump((n,str(pckt)),chkfile)
        nbytes += sport.write(pckt)
        n += 1
        slptime = 1/STDFREQ*(n)-time.clock()
        time.sleep(max(slptime,0)) # Maybe record time elapsed per cycle, and calc std Dev?
    ttot = time.clock()
    print ttot
    print sport.read()
    sport.close()
    print 'Total bytes written succssfully: ' + `nbytes`
    print 'Total time taken: ' + `ttot` + ' microseconds'
    print 'Avg time per packet: ' + `ttot/npackets*1e6` + 'microseconds'
    print 'Avg time deviation per write cycle: ' + `(1/STDFREQ-ttot/npackets)*1e6` + ' microseconds'
    print 'Percent error in packet duration: ' + `(1/STDFREQ-ttot/npackets)*STDFREQ*100` + '%'
    

main()