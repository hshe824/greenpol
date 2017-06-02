import os
import datetime as dt
import numpy as np
import h5py
import getData
import time
import sys
sys.path.append('../')
import config
#import connect

'''
conversions for angles, integer to degrees:
'''
#azgain=-360./(2.**16)    #az encoder is 16 bits natural binary 
#elgain=-360./(40000.)    #stupid encoder is BCD 18 bits 4 digits of 4 bits and one of two bits max 4x10x10x10x10
#eloffset=295.026         #updated based on moon crossing 2013/08/02, cofe 10 ghz ch37
#azoffset=4.41496+140.

azgain = config.azgain
elgain = config.elgain
eloffset = config.eloffset
azoffset = config.azoffset

degtoctsAZ = config.degtoctsAZ
degtoctsEl = config.degtoctsEl 

def bcd_to_int(bcd_str):
	string= ''
	return int(string.join([str(int(bcd_str[0:2],2)), str(int(bcd_str[2:6],2)), str(int(bcd_str[6:10],2)), str(int(bcd_str[10:14],2)), str(int(bcd_str[14:18],2))]))
	
def bin_to_int(bin_str):
	return int(bin_str,2)

def fileStruct(n_array, data):
	
	t=dt.datetime.now()
	folder = 'data_aquisition/data'
	date = t.strftime("%m-%d-%Y")
	time = t.strftime("%H-%M") #if you make a file more frequently than every minute, this will overwrite your data
	if not os.path.exists(folder +'/'+ date):#this is the first file being created for that time
		os.makedirs(folder +'/'+ date)
		#set index to 0
	
	path = '/'.join((folder, date,time))
	path = '.'.join((path,"h5"))
	
	#print(path)
	#fn = os.path.join(os.path.dirname(__file__), 'my_file')
	#Sprint(fn)
	if not os.path.exists(path):#every time we create a new file we wanna make sure it starts writting from the begining
		print(data.index)
		data.resetIndex()
	
	with h5py.File(str(path), 'w') as h5file:
		h5file.create_dataset("data", data=n_array)
		#set = h5file.create_dataset("data", (100, 100), 'i')
	
	

class datacollector(object):
	def __init__(self):
		self.index = 0
		self.free_space = 0
		self.data = np.zeros(self.free_space, dtype=[("el", np.float), ("az", np.float), ("rev", np.int)])
	def resetIndex(self):
		self.index=0
	def add(self,az,el,rev):
		if self.index>=self.free_space:
				self.data.resize(self.index+1000, 1)
				self.free_space = self.free_space+1000
		self.data[self.index] = ((az,el,rev))
		
		
		self.index =self.index+ 1
		
	def getData(self):
		return self.data
	

def getAzEl(eye):

	all = eye.getData()
	
	all = (bcd_to_int(all[0]), bin_to_int(all[1]), bin_to_int(all[2]))
	
	el=eloffset+elgain*all[0]
	az=np.mod(azoffset + azgain*all[1],360.)

	rev=all[2]

	return az, el, rev
	


#this is the offset between the optical beam and the galil
def offset(eye, c):
    azGalil = (float(c('TPX')) / degtoctsAZ) % 360.                            
    elGalil = (float(c('TPY')) / degtoctsEl) % 360.

    azBeam = getAzEl(eye)[0]
    elBeam = getAzEl(eye)[1]

    azOffset = azBeam - azGalil
    elOffset = elBeam - elGalil

    return azOffset, elOffset


#eye = getData.Eyeball()
#c = connect.g.GCommand
#global galilAzOffset
#galilAzOffset = offset(eye,c)[0]
#global galilElOffset
#galilElOffset = offset(eye,c)[1]

'''
if len(sys.argv)==1: #this is the defualt no argument write time
	sys.argv.append(60) #this sets how long it takes to write a file
#data = np.zeros(1000, dtype=[("first", np.int), ("second", np.int)])
eye = getData.Eyeball()
Data = datacollector()

#fileStruct(Data.getData()) 

time_a = time.time()

while True:
	#timer loop

	az, el, rev = getAzEl(eye)

	Data.add(el,az,rev)
	#print Data.getData()
	time_b = time.time()
	delta = time_b-time_a
	if (delta>=2):
		print(rev,az,el)
	if(delta>=int(sys.argv[1])): 
		fileStruct(Data.getData(), Data)
		time_a=time.time();
		print("file written")
		
print("data collected at" + str(1.0/delta) +"HZ")

		#print delta
		
		#time.sleep(.03-delta)
'''