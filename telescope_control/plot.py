import h5py as h5
import matplotlib.pyplot as plt
import numpy as np
from plot_path import open_folder
from plot_path import select_file

'''
Plot 3 variables hdf5 data in one figure
Given path of folder (characterized by year, month, and day)
Given path of files (characterized by a starting time and an ending time)
'''
def conti_test(year,month,day,st_hour,st_minute,ed_hour,ed_minute):
    
    d_h=ed_hour-st_hour
    d_m=ed_minute-st_minute
    time_range=abs(d_h)*60+abs(d_m)
    
    open_folder(month,day,year)
    files=select_file(month, day, year, st_hour,st_minute,ed_hour,ed_minute)

    minute=[]
    for i in range(len(files)):
        minute.append(int(files[i][0:2])*60+int(files[i][3:5]))
	
    print('# of files:',len(minute))
    print('Time range:',time_range)
	
    if len(minute)!=time_range:
        print "Files are discontinuous"

        return minute
    else:
        print 'Files are continuous'
        
        return minute




def plot_h5(var, year, month, day,st_hour,st_minute,ed_hour,ed_minute):
    
    open_folder(month,day,year)
    files=select_file(month, day, year, st_hour,st_minute,ed_hour,ed_minute)
    m=conti_test(year,month,day,st_hour,st_minute,ed_hour,ed_minute)
    
    numb=len(files)
    size=0
    i=0
    d_h=st_hour-ed_hour
    d_m=st_hour-ed_minute
    for fname in files:
        with h5.File(fname,'r') as f:
            var1 = f['data']['%s' % var]
##            var1 = f['data']['%s' % var]
            #el=f['data']['el']
            #az=f['data']['az']
            t=f['data']['gpstime']
            size=len(var1)
	   # print min(t), max(t)

        #t=np.linspace(int(m[i-1]),1+int(m[i-1]),size)
        

        #el,=plt.plot(t,el,'b',label='el')
        #az,=plt.plot(t,az,'k',label='az')
        #rev,=plt.plot(t,rev,'r--',label='rev')
	izero = np.where(t != 0)[0]
	t = t[izero]
	var1 = var1[izero]

	plt.plot(t, var1, 'b-', linewidth = 2)
	plt.ylabel('%s (deg)' % var)
	plt.xlabel('gps time')
        #plt.legend(handles=[el,az,rev])
    plt.show()
'''
if __name__=="__main__":
    plot_h5('el',2017,04,20,15,42,17,20)
'''
