import glob
import os
import sys


##keep format like "2017-05-16"; otherwise it returns "5" when you type "05"
def date_conv(year,month,day):
    m=[str(year),str(month),str(day)]
    for i in range(len(m)):
        if len(m[i])<2:
            m[i]=m[i].zfill(2)
    return m

##keep format like 01-02
def time_conv(st_hour,st_minute,ed_hour,ed_minute):
    n=[str(st_hour),str(st_minute),str(ed_hour),str(ed_minute)]
    for i in range(len(n)):
        if len(n[i])<2:
            n[i]=n[i].zfill(2)
    return n
    
##open folder of selected path
def open_folder(month, day, year):

    date=date_conv(month,day,year)
    
    #change the basic path "C:/Python27/deepspace/" to whatever you need            
    #os.chdir("C:/Users/labuser/Desktop/telescope_control/data_aquisition/data"+date[0]+"-"+date[1]+"-"+date[2])
    os.chdir("data_aquisition/data/"+date[0]+"-"+date[1]+"-"+date[2])

##select a staring-time and an ending-time, it returns hdf5 files in between
def select_file(st_hour,st_minute,ed_hour,ed_minute):
    
    #searching all hdf5 files under selected path
    files=glob.glob('*.hdf5')

    all_fname=[]

    #extract filename without extension
    for i in range(len(files)):
        all_fname.append(os.path.splitext(files[i])[0])

    ftime=time_conv(st_hour,st_minute,ed_hour,ed_minute)

    sub_fname=[]
    
    star=ftime[0]+"-"+ftime[1]
    end=ftime[2]+"-"+ftime[3]
    
    #search files between selected starting-time and ending-time
    for j in range(len(all_fname)):
        if all_fname[j]>star and all_fname[j]<end:
            sub_fname.append(files[j])
    return sub_fname