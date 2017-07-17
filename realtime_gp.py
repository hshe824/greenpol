"""
set of scripts to run while taking data for first look analysis
(run from main ground_cofe directory so paths work out right"""
import sys
sys.path.append('../')
sys.path.append('D:\software_git_repos\greenpol\telescope_control')
sys.path.append('D:\software_git_repos\greenpol\cofe-python-analysis-tools-master\utils_meinhold')
sys.path.append('D:\software_git_repos\greenpol\cofe-python-analysis-tools-master\utils_zonca')
from glob import glob
import os
import matplotlib.pyplot as plt
#import cofe_util as cu
import demod
import h5py
import cPickle
import numpy as np
from numpy.lib import recfunctions as recf
import matplotlib.pyplot as plt
from plot_path import *
from prm_util import nps
samprate=27.  #assumed spin rate of pol modulator for rough time estimation inside files

def get_h5_pointing(filelist,startrev=None, stoprev=None,angles_in_ints=False,azel_era=3):
    """
        modify to fast version, dont' average the multiple values, just take the first one. will cause a little bias but its very fast.
    also implmented removal of erroneous endof h5 file crap, and az outliers
    azel_era determines what az/el offsets to use, 1 means before 9/26/2013, 2 means 9/26-10/3 (inclusive), 3 means after 10/4.
    """
    
    #filelist is complete path list to the h5 files
    elconversion=-360./40000.
    azconversion=-360./(2.**16)
    #eloffset=8.2-3.17382
    eloffset=5.026 # correction from 2013/08/02 moon crossing for both az and el this for ch 3! 
    azoffset=4.41496
    # on 2013/08/20, updated converter.py to include these offsets, in theory they should now be zero.
    eloffset =0.0
    azoffset=0.0
    #ch1 would be azoffset=198.7810-187.663   or 11.118
    #             eloffset= 8.2-5.69175  
    #             eloffset= 2.5082
    #note October 4, 2013. Just found that data from 9/26/13 through 10/04/13 used old converter.py. So special 
    #offsets needed:
    #update, 10/8/13. ran get_cofe_crossing on second sun crossing from 10/04 (after subtracting 
    #template estimate of satellites,important effect). delta offsets: az=2.10,el=0.934
    #these then would be future offsets
    #update, 11/19/13. Ran mapmaking on lots of days, found an offset in the two daily crossings of the Crab- used ephem
    #to find the crossings, found that should get a self-consistent solution for both if the azimth is reduced by 4.51 degrees
    #and the elevation is increased by  2.241 degrees.
    
    if azel_era==1:
        eloffset=5.026
        azoffset=4.41496+140.0
    if azel_era==2:
        eloffset=5.026+0.934
        azoffset=4.41496+140.0+2.1
    if azel_era==3:
        eloffset=0.934+2.241
        azoffset=2.10 -4.51
    
    
    
    errlimit=0.1
    if angles_in_ints==True:
        errlimit=10
    hpointing=[]
    filelist.sort()
    for f in filelist:
        stats=os.stat(f)
        if stats.st_size<150000:
            print f,stats.st_size
        if stats.st_size > 150000:
            #print(f)
            h=h5py.File(f)
            hh=h['data']
            hpointing.append(hh[hh['gpstime']>=hh['gpstime'][0]])
            h.close()
    
    hpointing = np.concatenate(hpointing)
    #cut out blank lines from unfilled files
    if startrev != None:
        hpointing=hpointing[hpointing['gpstime'] > startrev]
    if stoprev != None:
        hpointing=hpointing[hpointing['gpstime'] < stoprev]

    hrevlist,inds=np.unique(hpointing['gpstime'],return_index=True)
    elmeans=hpointing['el'][inds]
    azmeans=hpointing['az'][inds]
    #get rid of az outliers:
    
    azmeans=np.mod(azmeans+azoffset,360.)
    elmeans=np.mod(elmeans+eloffset,90.)
    daz=np.diff(azmeans)
    
    badaz=np.unique(np.where(np.logical_and((np.abs(daz) > 5.) , (np.abs(daz+359.5) > 5.)))[0])
    if len(badaz > 1):
        if (badaz[-1]-len(daz) < 3):
            badaz=badaz[:-1]
        if (badaz[0] < 3):
            badaz=badaz[1:]
        azmeans[badaz]=(azmeans[badaz-2]+azmeans[badaz+2])/2.0
    azmeans=np.mod(azmeans,360.)
    return {'el':elmeans,'az':azmeans,'gpstime':hrevlist}



def get_demodulated_data_from_list(filelist,freq=10,supply_index=True,phase_offset=0):
    #print(filelist)
    filelist.sort() #just in case
    
    dd=[]
    for f in filelist:
        #only use full size files
        stats=os.stat(f)
        #print(stats.st_size)
        if stats.st_size == 10752000:
            #print f
            d=demod.demodulate_dat(f,freq,supply_index=True,phase_offset=phase_offset)
            #filename is start of data taking (I think) and we'll just add 1/samprate seconds per rev
            h=np.float64(f[-12:-10])
            m=np.float64(f[-10:-8])
            s=np.float64(f[-8:-6])
            t=h+m/60.+(s+(d['rev']-d['rev'][0])/samprate)/3600.
            d=recf.append_fields(d,'localtime',t)
            ut=np.mod(t+7.,24.)
            if len(f)>21:
                y=np.zeros(len(d),dtype=np.int)+np.int(f[-21:-17])
                mo=np.zeros(len(d),dtype=np.int)+np.int(f[-17:-15])
                dy=np.zeros(len(d),dtype=np.int)+np.int(f[-15:-13])
                ut=np.mod(t+7.,24.)
                utt=t+7.
                dy[utt>ut]=dy[utt>ut]+1
                d=recf.append_fields(d,['year','month','day'],[y,mo,dy])
            d=recf.append_fields(d,'ut',ut)
            dd.append(d)
    #print len(np.concatenate(dd))
    return np.concatenate(dd)
    
def combine_cofe_h5_pointing(dd,h5pointing,outfile='combined_data.pkl'):
    """
    combine demodulated data (output of get_demodulated_data_from_list) with H5 pointing data 
    (output of get_h5_pointing), dump to a pkl file by default (this takes a long time to run)
    """
    paz=h5pointing['az'].copy()
    prev=h5pointing['gpstime'].copy()
    #print(prev[0])
    #need to use only 24 bits for comparison with science data gpstime- probably a better way to do this, bitmasking?
    prev  &= 0x00ffffff
    #print(prev[0])
    pazw=np.where(abs(np.diff(paz) + 359.5)  < 3)[0]   #find the wrapping points so we can unroll the az for interpolation
    for r in pazw:
        paz[r+1:]=paz[r+1:]+360.                   #unwrap az
    azout=np.interp(dd['rev'],prev,paz)
    azout=np.mod(azout,360.)
    elout=np.interp(dd['rev'],prev,h5pointing['el'])
    f=open(outfile,'wb')
    combined_data={'sci_data':dd,'az': azout,'el':elout}
    cPickle.dump(combined_data,f,protocol=-1)
    f.close()
    return combined_data
    
def bin_to_az_el(indata,nazbins=360,nelbins=90,chan='ch3',cmode='T',revlimits=[0,2**24]):
    """
    straight binning code for data that's been associated with H5 pointing
    assume combined_dict came from combine_cofe_h5_pointing, that az and el are in degrees
    """
    
    azhalfbin=360./(nazbins*2.0)
    elhalfbin=90./(nelbins*2.0)
    azlist=np.arange(nazbins)*360./nazbins
    ellist=np.arange(nelbins)*90./nelbins
    chandata=-indata['sci_data'][chan][cmode][np.logical_and(indata['sci_data']['rev'] > revlimits[0],indata['sci_data']['rev']< revlimits[1])]
    eldata=indata['el'][np.logical_and(indata['sci_data']['rev'] > revlimits[0],indata['sci_data']['rev']< revlimits[1])]
    azdata=360.-indata['az'][np.logical_and(indata['sci_data']['rev'] > revlimits[0],indata['sci_data']['rev']< revlimits[1])]
    # make empty output map
    outmap=np.zeros([nazbins,nelbins],dtype=np.float64) 
    for x,azi in enumerate(azlist):
        for y,eli in enumerate(ellist):
            outmap[x,y]=np.mean(chandata[np.logical_and(abs(eldata-eli) < elhalfbin,abs(azdata-azi) < azhalfbin)])
    mapoffset=np.nanmin(outmap)
    outmap=np.nan_to_num(outmap-mapoffset)
    return outmap


def plotnow(fpath,yrmoday,chan,var,st_hour,st_minute,ed_hour,ed_minute,supply_index=False):
    """
    function to automatically read last 2 science files and last few pointing
    files, combine and plot signal vs azimuth. yrmoday should be a string
    '20130502' fpath should point to the 
    spot where acq_tel and converter.py were run
    """
    flp=select_h5(fpath,yrmoday,st_hour,st_minute,ed_hour,ed_minute)
    fld=select_dat(fpath,yrmoday,st_hour,st_minute,ed_hour,ed_minute)
    i=0
    while len(flp)<3:
        i+=1
        flp=select_h5(fpath,yrmoday,st_hour,int(st_minute)-i,ed_hour,int(ed_minute)+i)
    #~ print('Number of h5:',len(flp))
    #~ print('Initial h5:',flp[0][-11:][:5])
    #~ print('Final h5:',flp[-1][-11:][:5])
    #~ print('Number of dat:',len(fld))
    #~ print('Initial dat:',fld[0][-12:][:4])
    #~ print('Final dat:',fld[-1][-12:][:4])
    pp=get_h5_pointing(flp)
    dd=get_demodulated_data_from_list(fld,supply_index=supply_index)
    combined=combine_cofe_h5_pointing(dd,pp)
    plt.plot(combined['az'],combined['sci_data'][chan][var],label=chan)
    plt.xlabel('Azimuth angle, degrees')
    plt.ylabel('Signal, V')
    plt.title(chan+' COFE data binned to azimuth, date: '+fld[-1][-21:-13])
    plt.legend()
    plt.grid()
    plt.show()
    return combined

def plotnow_all(fpath,yrmoday,chan,var,st_hour,st_minute,ed_hour,ed_minute,supply_index=False):
    flp=select_h5(fpath,yrmoday,st_hour,st_minute,ed_hour,ed_minute)
    fld=select_dat(fpath,yrmoday,st_hour,st_minute,ed_hour,ed_minute)
    i=0
    while len(flp)<3:
        i+=1
        flp=select_h5(fpath,yrmoday,st_hour,int(st_minute)-i,ed_hour,int(ed_minute)+i)
    #~ print('Number of h5:',len(flp))
    #~ print('Initial h5:',flp[0][-11:][:5])
    #~ print('Final h5:',flp[-1][-11:][:5])
    #~ print('Number of dat:',len(fld))
    #~ print('Initial dat:',fld[0][-12:][:4])
    #~ print('Final dat:',fld[-1][-12:][:4])
    pp=get_h5_pointing(flp)
    dd=get_demodulated_data_from_list(fld,supply_index=supply_index)
    combined=combine_cofe_h5_pointing(dd,pp)

    for c in range(16):
        ch='ch%s' %str(c)
        plt.plot(combined['az'],combined['sci_data'][ch][var],label=ch)
    plt.xlabel('Azimuth angle, degrees')
    plt.ylabel('Signal, V')
    plt.title('All COFE data binned to azimuth, date: '+fld[-1][-21:-13])
    plt.legend(bbox_to_anchor=(1,1),loc=2,borderaxespad=0)
    plt.grid()
    plt.show()
    return combined

def plotnow_psd(fpath,yrmoday,chan,var,st_hour,st_minute,ed_hour,ed_minute,supply_index=False):
    """
    function to automatically read last 2 science files and last few pointing
    files, combine and plot signal vs azimuth. yrmoday should be a string
    '20130502' fpath should point to the 
    spot where acq_tel and converter.py were run
    """
    fs=30*256
    flp=select_h5(fpath,yrmoday,st_hour,st_minute,ed_hour,ed_minute)
    fld=select_dat(fpath,yrmoday,st_hour,st_minute,ed_hour,ed_minute)
    i=0
    while len(flp)<3:
        i+=1
        flp=select_h5(fpath,yrmoday,st_hour,int(st_minute)-i,ed_hour,int(ed_minute)+i)
#~ ##    print('Number of h5:',len(flp))
    #~ print('Initial h5:',flp[0][-11:][:5])
    #~ print('Final h5:',flp[-1][-11:][:5])
#~ ##    print('Number of dat:',len(fld))
    #~ print('Initial dat:',fld[0][-12:][:4])
    #~ print('Final dat:',fld[-1][-12:][:4])
    pp=get_h5_pointing(flp)
    dd=get_demodulated_data_from_list(fld,supply_index=supply_index)
    combined=combine_cofe_h5_pointing(dd,pp)
    #plt.psd(combined['sci_data'][chan][var],Fs=fs)
    
    freqs,pxx=nps(combined['sci_data'][chan][var],Fs=fs)
##    plt.ylabel('Power Spectral Density ' + var +r'$^2$/Hz')
##    plt.show()
##    freqs,pxx=nps(combined['sci_data'][chan][var],fsreturn freqs,pxx
    plt.plot(freqs,pxx,label=chan)
    plt.legend(bbox_to_anchor=(1,1),loc=2,borderaxespad=0)
    plt.show()
    return freqs,pxx



def plotnow_psd_all(fpath,yrmoday,chan,var,st_hour,st_minute,ed_hour,ed_minute,supply_index=False):
    flp=select_h5(fpath,yrmoday,st_hour,st_minute,ed_hour,ed_minute)
    fld=select_dat(fpath,yrmoday,st_hour,st_minute,ed_hour,ed_minute)
    i=0
    while len(flp)<3:
        i+=1
        flp=select_h5(fpath,yrmoday,st_hour,int(st_minute)-i,ed_hour,int(ed_minute)+i)
    #~ print('Number of h5:',len(flp))
    #~ print('Initial h5:',flp[0][-11:][:5])
    #~ print('Final h5:',flp[-1][-11:][:5])
    #~ print('Number of dat:',len(fld))
    #~ print('Initial dat:',fld[0][-12:][:4])
    #~ print('Final dat:',fld[-1][-12:][:4])
    pp=get_h5_pointing(flp)
    dd=get_demodulated_data_from_list(fld,supply_index=supply_index)
    combined=combine_cofe_h5_pointing(dd,pp)
    fs=30*256
    for c in range(16):
        ch='ch%s' %str(c)
        #plt.psd(combined['sci_data'][ch][var])
        freqs,pxx=nps(combined['sci_data'][ch][var],Fs=fs)
##    plt.ylabel('Power Spectral Density ' + var +r'$^2$/Hz')
##    plt.show()
##    freqs,pxx=nps(combined['sci_data'][chan][var],fsreturn freqs,pxx
        plt.plot(freqs,pxx,label=ch)
    plt.legend(bbox_to_anchor=(1,1),loc=2,borderaxespad=0)
    plt.show()
    return freqs,pxx
        

def plotrawnow(yrmoday,chan,var,path,rstep=50,supply_index=False):
    """
    function to automatically read last science file plot raw data vs encoder
    yrmoday should be a string '20130502' fpath should point to the 
    directory where acq_tel and converter.py were run
    rstep determines how many revolutions to skip between plotted revolutions
    """
    fld=glob(fpath+'data/'+yrmoday+'/*.dat')
    fld.sort()
    stats=os.stat(fld[-1])
    if stats.st_size == 10752000:
        dr=demod.read_raw([fld[-1]],supply_index=supply_index)
        for i in range(0,np.shape(dr[chan])[0],rstep):
            plt.plot(dr[chan][i,:],label='rev '+str(i))
        plt.xlabel('encoder position')
        plt.ylabel('Signal V')
        plt.title(chan+' Raw data, every '+str(rstep) + ' revs, file: '+fld[-1])
        plt.legend()
        plt.grid()
        plt.show()
    return dr
    
def psmapcurrent(cdata,chan='ch2',cmode='T',nbins=360):
    """
    function to combine already read science files and pointing
    files, and create pseudomap. chan is 'ch2', cmode is 'T'
    """
    combined = combine_cofe_h5_pointing(cdata['dd'],cdata['pp'])
    psmap=cu.phasebin(nbins,combined['az'],combined['sci_data'][chan][cmode])
    pcolormesh(psmap.T)
    return psmap
    
def getdatanow(yrmoday,fpath='',combined=True,phase_offset=0):
    """
    function to automatically read all science files and pointing
    files, save for future use, also save last h5 and .dat filenamesc
    yrmoday should be a string
    '20130502' fpath should point to the  spot where acq_tel and converter.py were run
    chan is 'ch2', cmode is 'T'
    """
    fld=glob(fpath+'data/'+yrmoday+'/*.dat')
    fld.sort()
    flp=glob(fpath+yrmoday[4:6]+'-'+yrmoday[6:8]+'-'+yrmoday[0:4]+'/*.h5')
    flp.sort()
    pp=get_h5_pointing(flp)
    dd=get_demodulated_data_from_list(fld,phase_offset=phase_offset)
    curr_data={'pp':pp,'dd':dd,'lastpfile':flp[-1],'lastdfile':fld[-1],'yrmoday':yrmoday,'fpath':fpath}
    if combined:
        curr_data=combine_cofe_h5_pointing(curr_data['dd'],curr_data['pp'],outfile='combined_data'+yrmoday+'.pkl')
    return curr_data
    
def combine_cdata(curr_data):
    """
    convenience function to use curr_data info to get combined data
    """
    combined=combine_cofe_h5_pointing(curr_data['dd'],curr_data['pp'],outfile='combined_data'+curr_data['yrmoday']+'.pkl')
    return combined

def updatedata(cdata):
    """
    function to automatically read all science files and pointing
    files, save for future use, also save last h5 and .dat filenamesc
    yrmoday should be a string
    '20130502' fpath should point to the  spot where acq_tel and converter.py were run
    chan is 'ch2', cmode is 'T'
    """
    fld=glob(cdata['fpath']+'data/'+cdata['yrmoday']+'/*.dat')
    fld.sort()
    flda=np.array(fld)
    flp=glob(cdata['fpath']+cdata['yrmoday'][4:6]+'-'+cdata['yrmoday'][6:8]+'-'+cdata['yrmoday'][0:4]+'/*.h5')
    flp.sort()
    flpa=np.array(flp)
    if fld[-1]>cdata['lastdfile']:
        dd=get_demodulated_data_from_list(flda[flda>cdata['lastdfile']])
        cdata['dd']=np.concatenate([cdata['dd'],dd])
        cdata['lastdfile']=fld[-1]
    if flp[-1]>cdata['lastpfile']:
        pp=get_h5_pointing(flpa[flpa>cdata['lastpfile']])
        cdata['pp']['az']=np.concatenate([cdata['pp']['az'],pp['az']])
        cdata['pp']['el']=np.concatenate([cdata['pp']['el'],pp['el']])
        cdata['pp']['rev']=np.concatenate([cdata['pp']['rev'],pp['rev']])
        cdata['lastpfile']=flp[-1]
    return cdata
def pointing_plot(var,vector,gpstime):
    plt.plot(gpstime,vector,label=str(var))
    plt.xlabel('gpstime')
    plt.ylabel(str(var))
    plt.title(str(var)+' ' + 'vs. gpstime')
    plt.legend()
    plt.grid()
    plt.show()
if __name__=="__main__":
    yrmoday='20170602'
    fpath='D:/software_git_repos/greenpol/telescope_control/'
    chan='ch2'
    var='T'
    freqs,pxx=plotnow_psd(fpath,yrmoday,chan,var,18,15,22,22)
##    freqs=freqs[0:10],pxx=pxx[0:10]
    print freqs,pxx
    plt.plot(freqs,pxx,'bo')
    plt.show()

