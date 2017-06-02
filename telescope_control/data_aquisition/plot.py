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

def plot_h5(var, year, month, day,st_hour,st_minute,ed_hour,ed_minute):
    
    open_folder(month,day,year)
    files=select_file(st_hour,st_minute,ed_hour,ed_minute)

    numb=len(files)

    el=[]
    az=[]
    rev=[]

    for fname in files:
        with h5.File(fname,'r') as f:
            var1=f['dataset'][0,:] #change dataset link 'dataset' according to your hdf5 configuration
            var2=f['dataset'][1,:]
            var3=f['dataset'][2,:]
            

        el.append(var1)
        az.append(var2)
        rev.append(var3)

    size=len(el)

    vars = dict(
        el=np.array(el).reshape(size,1),
        az=np.array(az).reshape(size,1),
        rev=np.array(rev).reshape(size,1)
    )
    t=np.linspace(0.0,numb,size)

#change variable name (y1,y2,y3) to anything you want
    #y1,=plt.plot(t,el,'b',label='y1')
    #y2,=plt.plot(t,az,'k',label='y2')
    #y3,=plt.plot(t,rev,'r--',label='y3')
    plt.plot(t, vars[var], 'b-', linewidth=2)
    plt.xlabel('Time(minute)')
    plt.ylabel('%s' % var)
    #plt.legend(handles=[y1,y2,y3])
    plt.show()

if __name__=="__main__":
    plot_h5('el',2017,04,20,15,42,15,43)