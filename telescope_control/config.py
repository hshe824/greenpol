#control paramters
import pickle
import os

fpath='D:/software_git_repos/greenpol/telescope_control/configurations/config'
#fpath='C:/Users/labuser/Desktop/greenpol-ari/telescope_control/configurations/config'
os.chdir(fpath)

def update_config():
    with open('config.txt','r') as handle:
        config=pickle.loads(handle.read())

        global global_location
        global_location=config['location']

        # deg to ct conversion for each motor
        global degtoctsAZ 
        degtoctsAZ = config['degtoctsAZ']
        global degtoctsEl 
        degtoctsEl = config['degtoctsEL']
            
        #azimuth scan settings
        global azSP 
        azSP = config['azSP'] * degtoctsAZ # az scan speed, 90 deg/sec
        global azAC
        azAC =  config['azAC'] * degtoctsAZ # acceleration 
        global azDC
        azDC =  config['azDC'] * degtoctsAZ # deceleration

        #elevation settings
        global elevSP
        elevSP = config['elevSP'] * degtoctsEl # x degrees/sec
        global elevAC
        elevAC = config['elevAC'] * degtoctsEl # acceleration 
        global elevDC
        elevDC = config['elevDC'] * degtoctsEl # deceleration

        #azimuth move settings
        global azSPm 
        azSPm = config['azSPm'] * degtoctsAZ # az scan speed, 90 deg/sec

        #gain and offset settings (ffset between encoder and beam)
        global azgain
        azgain=config['azgain']    #az encoder is 16 bits natural binary 
        global elgain
        elgain=config['elgain']    #stupid encoder is BCD 18 bits 4 digits of 4 bits and one of two bits max 4x10x10x10x10
        global eloffset
        eloffset=config['eloffset']         #updated based on moon crossing 2013/08/02, cofe 10 ghz ch37
        global azoffset
        azoffset=config['azoffset']
