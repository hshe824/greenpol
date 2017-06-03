#control paramters

# deg to ct conversion for each motor
global degtoctsAZ 
degtoctsAZ = 1024000./360.
global degtoctsEl 
degtoctsEl = 4096./360.
    
#azimuth scan settings
global azSP 
azSP = 5 * degtoctsAZ # az scan speed, 90 deg/sec
global azAC
azAC = 180 * degtoctsAZ # acceleration 
global azDC
azDC = azAC # deceleration

#elevation settings
global elevSP
elevSP = 5 * degtoctsEl # x degrees/sec
global elevAC
elevAC = 360 * degtoctsAZ # acceleration 
global elevDC
elevDC = elevAC # deceleration

#azimuth move settings
global azSPm 
azSPm = 5 * degtoctsAZ # az scan speed, 90 deg/sec

#gain and offset settings (ffset between encoder and beam)
global azgain
azgain=-360./(2.**16)    #az encoder is 16 bits natural binary 
global elgain
elgain=-360./(40000.)    #stupid encoder is BCD 18 bits 4 digits of 4 bits and one of two bits max 4x10x10x10x10
global eloffset
eloffset=295.026         #updated based on moon crossing 2013/08/02, cofe 10 ghz ch37
global azoffset
azoffset=4.41496+140.

