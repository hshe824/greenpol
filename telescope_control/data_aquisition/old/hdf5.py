import serial
import time
import datetime
import h5py
import numpy as np

def scan_usb():
    """find usb names and arrange them by 'COM' + str(i)"""
    available = []
    for i in range(256):
        try:
            s = serial.Serial('COM'+str(i))
            available.append( (s.portstr))
            s.close()  
        except serial.SerialException:
            pass

    return available

#find the creating time of the file
def file_time():
    timestr = time.strftime("%Y_%m_%d_%H_%M_%S")
    return timestr

#create txt file named by time
fileCreateTime = file_time()


#serial parameters
bytesize=8,
packetsize=50,
STDFREQ = 1/(120.e-6), #Number of packets per second

#choose the first comport("scan_usb()[0]" ) as the input
ser=serial.Serial(
    scan_usb()[0],
    baudrate=115200,
    timeout=3)
##ser.bytesize=serial.EIGHTBITS,
##ser.parity=serial.PARITY_EVEN,
##ser.stopbit=serial.STOPBITS_ONE,


if ser.isOpen == False:
    ser.open()
    ser.write("serial is turning on")
    
# file counter for while loop
j=0



while True:
    line=np.zeros(5000)
    j+=1
#break when no data sending from the serial
    if len(ser.read(1))==0:
        print("no signal")
        ser.close()
        break

#create hdf5 files
    with h5py.File(fileCreateTime+"_"+str(j)+".hdf5","w") as f:
#dataset structure: 50 variables(as Nic's index suggests) , 100 data per variable
        dset=f.create_dataset('nicdata',(50,100))
#file size: 5000 units
        for i in range(5000):
#read data one by one byte and convert it to an integer 
            temp=ord(ser.read(1))
#fill data in the blank array 
            line[i]=temp

"""Attention!!!
Here is an issue:
if I add 50 attributes
it runs very slow"""
##            if line[i-50]==0:
##                dset.attrs["STRT0"]=line[i-50]
##                dset.attrs["STRT1"]=line[i-49]
##                dset.attrs["GPS0"]=line[i-48]
##                dset.attrs["GPS1"]=line[i-47]
##                dset.attrs["GPS2"]=line[i-46]
##                dset.attrs["GPS3"]=line[i-45]
##                dset.attrs["STAT0"]=line[i-44]
##                dset.attrs["POL0"]=line[i-43]
##                dset.attrs["POL1"]=line[i-42]
##                dset.attrs["EL0"]=line[i-41]
##                dset.attrs["EL1"]=line[i-40]
##                dset.attrs["EL2"]=line[i-39]
##                dset.attrs["ADC0_CH0_BO"]=line[i-38]
##                dset.attrs["ADC0_CH0_B1"]=line[i-37]
##                dset.attrs["ADC0_CH1_BO"]=line[i-36]
##                dset.attrs["ADC0_CH1_B1"]=line[i-35]
##                dset.attrs["ADC0_CH2_BO"]=line[i-34]
##                dset.attrs["ADC0_CH2_B1"]=line[i-33]
##                dset.attrs["ADC0_CH3_BO"]=line[i-32]
##                dset.attrs["ADC0_CH3_B1"]=line[i-31]
##                dset.attrs["ADC0_CH4_BO"]=line[i-30]
##                dset.attrs["ADC0_CH4_B1"]=line[i-29]
##                dset.attrs["ADC0_CH5_BO"]=line[i-28]
##                dset.attrs["ADC0_CH5_B1"]=line[i-27]
##                dset.attrs["ADC0_CH6_BO"]=line[i-26]
##                dset.attrs["ADC0_CH6_B1"]=line[i-25]
##                dset.attrs["ADC0_CH7_BO"]=line[i-24]
##                dset.attrs["ADC0_CH7_B1"]=line[i-23]
##                dset.attrs["ADC1_CH0_BO"]=line[i-22]
##                dset.attrs["ADC1_CH0_B1"]=line[i-21]
##                dset.attrs["ADC1_CH1_BO"]=line[i-20]
##                dset.attrs["ADC1_CH1_B1"]=line[i-19]
##                dset.attrs["ADC1_CH2_BO"]=line[i-18]
##                dset.attrs["ADC1_CH2_B1"]=line[i-17]
##                dset.attrs["ADC1_CH3_BO"]=line[i-16]
##                dset.attrs["ADC1_CH3_B1"]=line[i-15]
##                dset.attrs["ADC1_CH4_BO"]=line[i-14]
##                dset.attrs["ADC1_CH4_B1"]=line[i-13]
##                dset.attrs["ADC1_CH5_BO"]=line[i-12]
##                dset.attrs["ADC1_CH5_B1"]=line[i-11]
##                dset.attrs["ADC1_CH6_BO"]=line[i-10]
##                dset.attrs["ADC1_CH6_B1"]=line[i-9]
##                dset.attrs["ADC1_CH7_BO"]=line[i-8]
##                dset.attrs["ADC1_CH7_B1"]=line[i-7]
##                dset.attrs["AZ0"]=line[i-6]
##                dset.attrs["AZ1"]=line[i-5]
##                dset.attrs["AZ2"]=line[i-4]
##                dset.attrs["AZ3"]=line[i-3]
##                dset.attrs["END0"]=line[i-2]
##                dset.attrs["END1"]=line[i-1]
##            

#reshape array into 50X100 dataset
data=line.reshape(50,100)
#send data to hdf5
dset[:]=data
        #print dset[:]
#flush buffer
f.flush()

        


print("Mission Complete")