import config
config.update_config()
import scan
import moveto
import connect
import os
import sys
#sys.path.append('C:/Users/labuser/Desktop/python_temp')
sys.path.append('D:/software_git_repos/greenpol')
sys.path.append('C:/Python27/Lib/site-packages/')
#sys.path.append('C:/Python27x86/lib/site-packages')
sys.path.append('data_aquisition')
import get_pointing as gp
import gclib
import threading
import time
from time import strftime
import pickle
from datetime import datetime, timedelta
import numpy as np
#from tkinter import ttk #this is for python 3
#from tkinter import *   #this is for python 3
from Tkinter import *    #this is for python 2.7
import ttk #this is for python 2.7
import realtime_gp as rt
import matplotlib.pyplot as plt
from plot_path import *
import planets

g = connect.g
c = g.GCommand
##
g2 = connect.g2
c2 = g2.GCommand
#offset between galil and beam
offsetAz = gp.galilAzOffset 
offsetEl = gp.galilElOffset

degtoctsAZ = config.degtoctsAZ
degtoctsEl = config.degtoctsEl

global_location = config.global_location

class interface:

    def __init__(self, master):#, interval = 0.2): 

        mainFrame = Frame(master)
        mainFrame.pack()

        nb = ttk.Notebook(mainFrame)

        ##### azimuth scan #####
        page1 = Frame(nb)

        #topframe = Frame(page1)
        #topframe.pack(side=TOP)

        inputframe = Frame(page1)
        inputframe.pack(side=TOP)

        buttonframe = Frame(page1)
        buttonframe.pack(side=BOTTOM)

        #self.title = Label(topframe, text = 'Az Scan')
        #self.title.pack()

        self.l1 = Label(inputframe, text='Scan Time (seconds)')
        self.l1.grid(row = 0, column = 0, sticky=W)
        self.l4 = Label(inputframe, text='("inf" for continuous scan)')
        self.l4.grid(row = 1, column = 1, sticky=W)
        self.l2 = Label(inputframe, text='Iteration #')
        self.l2.grid(row = 2, column = 0, sticky=W)
        self.l3 = Label(inputframe, text='El Step Size (deg)')
        self.l3.grid(row = 3, column = 0, sticky=W)
        #self.l4 = Label(inputframe, text='Starting AZ (deg)')
        #self.l4.grid(row = 3, column = 0, sticky=W)
        #self.l5 = Label(inputframe, text='Starting EL (deg)')
        #self.l5.grid(row = 4, column = 0, sticky=W)

        #user input
        self.tscan = Entry(inputframe)
        self.tscan.insert(END, 'inf')
        self.tscan.grid(row = 0, column = 1)

        self.iterations = Entry(inputframe)
        self.iterations.insert(END, '2')
        self.iterations.grid(row = 2, column = 1)

        self.deltaEl = Entry(inputframe)
        self.deltaEl.insert(END, '10.0')
        self.deltaEl.grid(row = 3, column = 1)

        #self.az0 = Entry(inputframe)
        #self.az0.insert(END, '0.0')
        #self.az0.grid(row = 3, column = 1)

        #self.el0 = Entry(inputframe)
        #self.el0.insert(END, '60.0')
        #self.el0.grid(row = 4, column = 1)

        self.scan = Button(buttonframe, 
            text='Start Scan', 
            command=self.scanAz)
        self.scan.pack(side=LEFT)


        ###### tracking  ######
        nb2 = ttk.Notebook(nb)

        ###### linear scan ######
        page2 = Frame(nb2)
        self.inputframe_lin = Frame(page2)
        self.inputframe_lin.pack(side=TOP)

        buttonframe = Frame(page2)
        buttonframe.pack(side=BOTTOM)

        self.l2 = Label(self.inputframe_lin, text='Celestial Object')
        self.l2.grid(row = 1, column = 0, sticky=W)
        self.l3 = Label(self.inputframe_lin, text='Az Scan #')
        self.l3.grid(row = 2, column = 0, sticky=W)
        self.l4 = Label(self.inputframe_lin, text='Min Az')
        self.l4.grid(row = 3, column = 0, sticky=W)
        self.l5 = Label(self.inputframe_lin, text='Max AZ')
        self.l5.grid(row = 4, column = 0, sticky=W)

        #user input

        self.numAzScans_lin = Entry(self.inputframe_lin,width=10)
        self.numAzScans_lin.insert(END, '2')
        self.numAzScans_lin.grid(row = 2, column = 1,sticky=W)

        self.MinAz_lin = Entry(self.inputframe_lin,width=10)
        self.MinAz_lin.insert(END, '-10.0')
        self.MinAz_lin.grid(row = 3, column = 1,sticky=W)

        self.MaxAz_lin = Entry(self.inputframe_lin,width=10)
        self.MaxAz_lin.insert(END, '10.0')
        self.MaxAz_lin.grid(row = 4, column = 1,sticky=W)


        ##########linear tracking drop down#######
        self.planets = ['Sky-Coord','Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune']
        self.cbody_lin=StringVar(self.inputframe_lin)
        self.cbody_lin.set(self.planets[1])
        self.phouse=OptionMenu(self.inputframe_lin,self.cbody_lin,*self.planets,command=self.update_cbody_lin)
        self.phouse.grid(row = 1, column = 1,sticky=W)

        self.scan = Button(buttonframe, 
            text='Start Scan', 
            command=self.linear)
        self.scan.pack(side=LEFT)

        ###### horizontal scan ######
        page3 = Frame(nb2)
        self.inputframe_hor = Frame(page3)
        self.inputframe_hor.pack(side=TOP)

        buttonframe = Frame(page3)
        buttonframe.pack(side=BOTTOM)

        self.l2 = Label(self.inputframe_hor, text='Celestial Object')
        self.l2.grid(row = 1, column = 0, sticky=W)
        self.l3 = Label(self.inputframe_hor, text='Az Scan #')
        self.l3.grid(row = 2, column = 0, sticky=W)
        self.l4 = Label(self.inputframe_hor, text='Min Az')
        self.l4.grid(row = 3, column = 0, sticky=W)
        self.l5 = Label(self.inputframe_hor, text='Max AZ')
        self.l5.grid(row = 4, column = 0, sticky=W)
        self.l6 = Label(self.inputframe_hor, text='Min El')
        self.l6.grid(row = 5, column = 0, sticky=W)
        self.l7 = Label(self.inputframe_hor, text='Max El')
        self.l7.grid(row = 6, column = 0, sticky=W)
        self.l8 = Label(self.inputframe_hor, text='Step Size')
        self.l8.grid(row = 7, column = 0, sticky=W)

        #user input
        self.numAzScans_hor = Entry(self.inputframe_hor,width=10)
        self.numAzScans_hor.insert(END, '2')
        self.numAzScans_hor.grid(row = 2, column = 1,sticky=W)

        self.MinAz_hor = Entry(self.inputframe_hor,width=10)
        self.MinAz_hor.insert(END, '-10.0')
        self.MinAz_hor.grid(row = 3, column = 1,sticky=W)

        self.MaxAz_hor = Entry(self.inputframe_hor,width=10)
        self.MaxAz_hor.insert(END, '10.0')
        self.MaxAz_hor.grid(row = 4, column = 1,sticky=W)

        self.MinEl = Entry(self.inputframe_hor,width=10)
        self.MinEl.insert(END, '-10.0')
        self.MinEl.grid(row = 5, column = 1,sticky=W)

        self.MaxEl = Entry(self.inputframe_hor,width=10)
        self.MaxEl.insert(END, '10.0')
        self.MaxEl.grid(row = 6, column = 1,sticky=W)

        self.stepSize = Entry(self.inputframe_hor,width=10)
        self.stepSize.insert(END, '10.0')
        self.stepSize.grid(row = 7, column = 1,sticky=W)


        
        ##########horizontal tracking drop down#######
        self.planets = ['Sky-Coord', 'Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune']
        self.cbody_hor=StringVar(self.inputframe_hor)
        self.cbody_hor.set(self.planets[1])
        self.phouse=OptionMenu(self.inputframe_hor,self.cbody_hor,*self.planets,command=self.update_cbody_hor)  
        self.phouse.grid(row = 1, column = 1,sticky=W)

        self.scan = Button(buttonframe, 
            text='Start Scan', 
            command=self.horizontal)
        self.scan.pack(side=LEFT)

        ####### move distance page #########
        movePage = Frame(nb)

        moveDFrame = Frame(movePage)
        moveDFrame.pack()

        movetoFrame = Frame(movePage)
        movetoFrame.pack(side=TOP)

        labelD = Label(moveDFrame, text = 'Move Distance')
        labelD.pack()

        inputframe = Frame(moveDFrame)
        inputframe.pack(side=TOP)

        buttonframe = Frame(moveDFrame)
        buttonframe.pack(side=BOTTOM)

        self.l1 = Label(inputframe, text='az')
        self.l1.grid(row = 0, column = 0, sticky=W)

        self.l2 = Label(inputframe, text='el')
        self.l2.grid(row = 2, column = 0, sticky=W)

        #user input
        self.az = Entry(inputframe,width=8)
        self.az.insert(END, '0.0')
        self.az.grid(row = 0, column = 1)

        self.el = Entry(inputframe,width=8)
        self.el.insert(END, '0.0')
        self.el.grid(row = 2, column = 1)

        
        plus_azdis = Button(inputframe, text="+",width=5, command=lambda:self.moveDist('+az')) 
        plus_azdis.grid(row=1, column=1, padx=2, pady=0, sticky="W")
        minus_azdis = Button(inputframe, text="-",width=5, command=lambda:self.moveDist('-az'))
        minus_azdis.grid(row=1, column=2, padx=2, pady=2, sticky="W")


        plus_eldis = Button(inputframe, text="+",width=5, command=lambda:self.moveDist('+el')) 
        plus_eldis.grid(row=3, column=1, padx=2, pady=0, sticky="W")
        minus_eldis = Button(inputframe, text="-",width=5, command=lambda:self.moveDist('-el'))
        minus_eldis.grid(row=3, column=2, sticky="W")

       ########## move to #############

        labelto = Label(movetoFrame, text = 'Move to Location')
        labelto.pack()

        self.inputframe2 = Frame(movetoFrame)
        self.inputframe2.pack(side=TOP)

        self.buttonframe2 = Frame(movetoFrame)
        self.buttonframe2.pack(side=BOTTOM)

        self.mtl1 = Label(self.inputframe2, text='az')
        self.mtl1.grid(row = 0, column = 0, sticky=W)

        self.mtl2 = Label(self.inputframe2, text='el')
        self.mtl2.grid(row = 1, column = 0, sticky=W)

        #user input
        self.az2 = Entry(self.inputframe2)
        self.az2.insert(END, '0.0')
        self.az2.grid(row = 0, column = 1)

        self.el2 = Entry(self.inputframe2)
        self.el2.insert(END, '0.0')
        self.el2.grid(row = 1, column = 1)

        self.scan = Button(self.buttonframe2, 
            text='Start Move', command=self.moveTo)
        self.scan.pack(side=LEFT)

        self.convert=Button(self.buttonframe2,
                            text='radec/azel',command=self.update_moveto)
        self.convert.pack(side=RIGHT)
########### configuration page ###################
        configPage=Frame(nb)
        configFrame=Frame(configPage)
        configFrame.pack()
        
        self.loclabel=Label(configFrame, text='Location')
        self.loclabel.grid(row=0, column=0, sticky=W)
        self.location=Entry(configFrame)
        self.location.grid(row=0, column=1)

        self.degtoctsAZ_l=Label(configFrame, text='degtoctsAZ')
        self.degtoctsAZ_l.grid(row=1, column=0, sticky=W)
        self.degtoctsAZ=Entry(configFrame)
        self.degtoctsAZ.grid(row=1, column=1)

        self.degtoctsEL_l=Label(configFrame, text='degtoctsEL')
        self.degtoctsEL_l.grid(row=2, column=0, sticky=W)
        self.degtoctsEL=Entry(configFrame)
        self.degtoctsEL.grid(row=2, column=1)

        self.azSP_l=Label(configFrame, text='azSP')
        self.azSP_l.grid(row=3, column=0, sticky=W)
        self.azSP=Entry(configFrame)
        self.azSP.grid(row=3, column=1)

        self.azAC_l=Label(configFrame, text='azAC')
        self.azAC_l.grid(row=4, column=0, sticky=W)
        self.azAC=Entry(configFrame)
        self.azAC.grid(row=4, column=1)

        self.azDC_l=Label(configFrame, text='azDC')
        self.azDC_l.grid(row=5, column=0, sticky=W)
        self.azDC=Entry(configFrame)
        self.azDC.grid(row=5, column=1)

        self.elevSP_l=Label(configFrame, text='elevSP')
        self.elevSP_l.grid(row=6, column=0, sticky=W)
        self.elevSP=Entry(configFrame)
        self.elevSP.grid(row=6, column=1)

        self.elevAC_l=Label(configFrame, text='elevAC')
        self.elevAC_l.grid(row=7, column=0, sticky=W)
        self.elevAC=Entry(configFrame)
        self.elevAC.grid(row=7, column=1)

        self.elevDC_l=Label(configFrame, text='elevDC')
        self.elevDC_l.grid(row=8, column=0, sticky=W)
        self.elevDC=Entry(configFrame)
        self.elevDC.grid(row=8, column=1)

        self.azSPm_l=Label(configFrame, text='azSPm')
        self.azSPm_l.grid(row=9, column=0, sticky=W)
        self.azSPm=Entry(configFrame)
        self.azSPm.grid(row=9,column=1)

        self.azgain_l=Label(configFrame, text='azgain')
        self.azgain_l.grid(row=10, column=0, sticky=W)
        self.azgain=Entry(configFrame)
        self.azgain.grid(row=10,column=1)

        self.elgain_l=Label(configFrame, text='elgain')
        self.elgain_l.grid(row=11, column=0, sticky=W)
        self.elgain=Entry(configFrame)
        self.elgain.grid(row=11,column=1)

        self.azoffset_l=Label(configFrame, text='azoffset')
        self.azoffset_l.grid(row=12, column=0, sticky=W)
        self.azoffset=Entry(configFrame)
        self.azoffset.grid(row=12,column=1)

        self.eloffset_l=Label(configFrame, text='eloffset')
        self.eloffset_l.grid(row=13, column=0, sticky=W)
        self.eloffset=Entry(configFrame)
        self.eloffset.grid(row=13,column=1)

        self.apply=Button(configFrame,text='Apply', command=self.global_config)
        self.apply.grid(row=14,column=1,sticky=W)
	
        fpath='D:/software_git_repos/greenpol/telescope_control/configurations/config'
        os.chdir(fpath)

        try:

            with open('config.txt', 'r') as handle:
                data=pickle.loads(handle.read())

		##configuration
		self.location.delete(0,'end')
		self.location.insert(END,data['location'])
		self.degtoctsAZ.delete(0,'end')
		self.degtoctsAZ.insert(END,data['degtoctsAZ'])
		self.degtoctsEL.delete(0,'end')
		self.degtoctsEL.insert(END,data['degtoctsEL'])
		self.azSP.delete(0,'end')
		self.azSP.insert(END,data['azSP'])
		self.azAC.delete(0,'end')
		self.azAC.insert(END,data['azAC'])
		self.azDC.delete(0,'end')
		self.azDC.insert(END,data['azDC'])
		self.elevSP.delete(0,'end')
		self.elevSP.insert(END,data['elevSP'])
		self.elevAC.delete(0,'end')
		self.elevAC.insert(END,data['elevAC'])
		self.elevDC.delete(0,'end')
		self.elevDC.insert(END,data['elevDC'])
		self.azSPm.delete(0,'end')
		self.azSPm.insert(END,data['azSPm'])
		self.azgain.delete(0,'end')
		self.azgain.insert(END,data['azgain'])
		self.elgain.delete(0,'end')
		self.elgain.insert(END,data['elgain'])
		self.azoffset.delete(0,'end')
		self.azoffset.insert(END,data['azoffset'])
		self.eloffset.delete(0,'end')
		self.eloffset.insert(END,data['eloffset'])
		
	except:
		pass

        ####### notebook layout #########
        nb.add(movePage, text='Move')
        nb.add(page1, text='Az Scan')
        nb.add(nb2, text='Track')
        nb.add(configPage,text='Configuration')
        nb2.add(page2, text = 'Linear Scan')
        nb2.add(page3, text = 'Horizontal Scan')


        nb.pack(expand=1, fill="both")

        ####### output frame ##### 

        outputframe = Frame(mainFrame)
        outputframe.pack()
        
        outputframe1 = Frame(outputframe)
        outputframe1.pack()

        outputframe2 = Frame(outputframe)
        outputframe2.pack()
        
        self.title = Label(outputframe1, text='Feedback')
        self.title.pack(side=LEFT)

        self.laz = Label(outputframe2, text='az')
        self.laz.grid(row = 0, column = 0, sticky = W)

        self.aztxt = Text(outputframe2, height = 1, width = 15)
        self.aztxt.grid(row = 0, column = 1)

        self.lalt = Label(outputframe2, text='el')
        self.lalt.grid(row = 1, column = 0, sticky = W)

        self.alttxt = Text(outputframe2, height = 1, width = 15)
        self.alttxt.grid(row = 1, column = 1)
        '''
        self.convertbutton = Button(mainFrame, text='RA/Dec', command=self.azel_to_radec)
        self.convertbutton.grid(row=2, column=0)
        self.fra = Text(outputframe2, height=1, width =5)
        self.fra.grid(row=2, column = 1)
        self.fdec = Text(outputframe2, height=1, width =5)
        self.fdec.grid(row=2, column = 2) 
        '''

        #ra dec output
        self.lra = Label(outputframe2, text='ra')
        self.lra.grid(row = 0, column = 2, sticky = W)
        self.ratxt = Text(outputframe2, height = 1, width = 15)
        self.ratxt.grid(row = 0, column = 3)
        self.ldec = Label(outputframe2, text='dec')
        self.ldec.grid(row = 1, column = 2, sticky = W)
        self.dectxt = Text(outputframe2, height = 1, width = 15)
        self.dectxt.grid(row = 1, column = 3)
        '''
        #galil output
        self.lazG = Label(outputframe2, text='az Galil')
        self.lazG.grid(row = 0, column = 2, sticky = W)
        self.aztxtG = Text(outputframe2, height = 1, width = 15)
        self.aztxtG.grid(row = 0, column = 3)
        self.laltG = Label(outputframe2, text='el Galil')
        self.laltG.grid(row = 1, column = 2, sticky = W)
        self.alttxtG = Text(outputframe2, height = 1, width = 15)
        self.alttxtG.grid(row = 1, column = 3)
        '''
        #thread stuff
        #self.interval = interval
        thread = threading.Thread(target=self.moniter, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()  
        
	'''
        thread = threading.Thread(target=self.moniterGalil, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start() 
	'''
        #plot data

        self.outputframe3 = Frame(outputframe)
        self.outputframe3.pack()

        self.scan = Button(self.outputframe3, 
            text='Plot', command=self.plot)
        self.scan.grid(row = 0, column = 0, sticky=W)


    
        self.l1 = Label(self.outputframe3, text='Date')
        self.l1.grid(row = 0, column = 2, sticky =W)
    
        self.date = Entry(self.outputframe3, width = 10)
        self.date.insert(END, '2017-06-02')
        self.date.grid(row = 0, column = 3)

        self.l2 = Label(self.outputframe3, text='From')
        self.l2.grid(row = 0, column = 4, sticky=W)

        self.beg = Entry(self.outputframe3, width = 5)
        self.beg.insert(END, '18-17')
        self.beg.grid(row = 0, column = 5)

        self.l3 = Label(self.outputframe3, text='To')
        self.l3.grid(row = 0, column = 6, sticky=W)
    
        self.end = Entry(self.outputframe3, width = 5)
        self.end.insert(END, '22-07')
        self.end.grid(row = 0, column = 7, sticky=W)

        self.l4 = Label(self.outputframe3, text='yyyy-mm-dd')
        self.l4.grid(row = 1, column = 3, sticky=W)
    
        self.l5 = Label(self.outputframe3, text='HH-MM')
        self.l5.grid(row = 1, column = 5, sticky=W)

        self.l6 = Label(self.outputframe3, text='HH-MM')
        self.l6.grid(row = 1, column =7, sticky=W)

        ############# plot drop down menu ###############
        #For Move Plot
        self.choice1=['az','el','gpstime','sci_data'] 
        self.bar1=StringVar()
        self.bar1.set(self.choice1[0])
        self.option1=OptionMenu(self.outputframe3,self.bar1,*self.choice1,command=self.update_ch)
        self.option1.grid(row=0,column=1,sticky=W)     

        ############# stop frame ###############
        
        #bottomFrame = Frame(mainFrame)
        #bottomFrame.pack(side=BOTTOM)

        self.stopbutton = Button(mainFrame, text='Stop', command=self.stop)
        self.stopbutton.pack(side=LEFT)

        self.quitButton = Button(mainFrame, text='Exit', command=master.quit)
        self.quitButton.pack(side=LEFT)

        self.motorTxt = Text(mainFrame, height = 1, width = 3)
        self.motorTxt.insert(END, 'ON')
        self.motorTxt.pack(side=RIGHT)
        
        self.motorButton = Button(mainFrame, text='Motor ON/OFF', command=self.motor)
        self.motorButton.pack(side=RIGHT)
	
	exebutton=Button(mainFrame, text='acq_tel',command=self.openexe)
	exebutton.pack(side=RIGHT)
        
        ###########Record and Load Configuration###########

        self.outputframe4 = Frame(outputframe)
        self.outputframe4.pack()
        self.backup_l = Entry(self.outputframe4, width=20)
        self.backup_l.grid(row=1,column=2,sticky=W)
        self.backup_l.insert(END,'Target Label')
        self.date_l=Entry(self.outputframe4, width=20)
        self.date_l.grid(row=1,column=1,sticky=W)
        labeltime=strftime("%Y-%m-%d")
        self.date_l.insert(END,labeltime)
##        self.backup_l.insert(END,'2017-06-26/00-00-00')
##        self.l1 = Label(mainFrame, text='yyyy-mm-dd/HH-MM-SS')
##        self.l1.pack(side=BOTTOM)
        self.loadbutton = Button (self.outputframe4, text='Load', command=self.read_txt)
        self.loadbutton.grid(row=1,column=0,sticky=W)
        
        self.backup_r = Entry(self.outputframe4, width=20)
        self.backup_r.grid(row=0,column=1,sticky=W)
        self.backup_r.insert(END,'Your Label')
        self.recordbutton = Button (self.outputframe4, text='Record', command=self.write_txt)
        self.recordbutton.grid(row=0,column=0,sticky=W)
	
	try:
		path='D:/software_git_repos/greenpol/telescope_control/configurations/memory/'
		os.chdir(path)
		all_subdirs = [d for d in os.listdir('.') if os.path.isdir(d)]
		latest_subdir = max(all_subdirs, key=os.path.getmtime)
		os.chdir(path+latest_subdir)
		list_of_files = glob.glob('*.txt')
		latest_file = max(list_of_files, key=os.path.getctime)
		fname=os.path.splitext(latest_file)[0]
		self.read(fname=fname,date=latest_subdir)
	except:
		pass

    def openexe(self):
		
	os.startfile('D:/software_git_repos/greenpol/telescope_control/data_aquisition/acq_tel.exe') #specify the path of .exe file
    
    def global_config(self):
        global_location=self.location.get()
        degtoctsAZ=eval(self.degtoctsAZ.get())
        degtoctsEL=eval(self.degtoctsEL.get())
        azSP=eval(self.azSP.get())
        azAC=eval(self.azAC.get())
        azDC=eval(self.azDC.get())
        elevSP=eval(self.elevSP.get())
        elevAC=eval(self.elevAC.get())
        elevDC=eval(self.elevDC.get())
        azSPm=eval(self.azSPm.get())
        azgain=eval(self.azgain.get())
        elgain=eval(self.elgain.get())
        azoffset=eval(self.azoffset.get())
        eloffset=eval(self.eloffset.get())       
        
        fpath='D:/software_git_repos/greenpol/telescope_control/configurations'
        os.chdir(fpath)
        folder='config'
        if not os.path.exists(folder):#this is the first file being created for that time
            os.makedirs(folder)
        os.chdir(fpath+'/'+folder)
        configuration={'location':global_location,'degtoctsAZ':degtoctsAZ,'degtoctsEL':degtoctsEL,
                'azSP':azSP,'azAC':azAC,'azDC':azDC,'elevSP':elevSP,'elevAC':elevAC,'elevDC':elevDC,
                'azSPm':azSPm,'azgain':azgain,'elgain':elgain,'azoffset':azoffset,'eloffset':eloffset}
        with open('config.txt', 'w') as handle:
                pickle.dump(configuration,handle)
        print 'Applying Configurations'
        config.update_config()
        

##                self.var.delete(0,'end')
##                self.var.insert(END,self.choices[i])

    def write_txt(self):
        cbody_lin=self.cbody_lin.get()
        cbody_hor=self.cbody_hor.get()
        mtlabel1=self.mtl1.cget('text')
        mtlabel2=self.mtl2.cget('text')

        if cbody_lin=='Sky-Coord':
            celestialcoor_lin=[cbody_lin, self.cor1_lin.get(), self.cor2_lin.get()]
        if cbody_lin!='Sky-Coord':
            celestialcoor_lin=cbody_lin

        if cbody_hor=='Sky-Coord':
            celestialcoor_hor=[cbody_hor, self.cor1_hor.get(), self.cor2_hor.get()]
        if cbody_hor!='Sky-Coord':
            celestialcoor_hor=cbody_hor
   
        
        data={'Move Distance':{'az':self.az.get(),'el':self.el.get()},
                   'Move to Location':{mtlabel1:self.az2.get(),mtlabel2:self.el2.get()},
                   'Az Scan':{'Scan Time':self.tscan.get(),'Iteration #':
                              self.iterations.get(),'El Step Size':self.deltaEl.get()},
                   'Linear Scan':{'Celestial Object':celestialcoor_lin,
                                  'Az Scan #':self.numAzScans_lin.get(),
                                  'Min Az':self.MinAz_lin.get(),
                                  'Max Az':self.MaxAz_lin.get()},
                   'Horizontal Scan':{'Celestial Object':celestialcoor_hor,
                                      'Az Scan #':self.numAzScans_hor.get(),
                                      'Min Az':self.MinAz_hor.get(),
                                      'Max Az':self.MaxAz_hor.get(),
                                      'Min El':self.MinEl.get(),
                                      'Max El':self.MaxEl.get(),
                                      'Step Size':self.stepSize.get()},
		      'Plot':{'Date':self.date.get(),
			      'From':self.beg.get(),
			      'To':self.end.get()}}

        date = strftime("%Y-%m-%d")
        time=strftime("%H-%M-%S")
        fpath='D:/software_git_repos/greenpol/telescope_control/configurations'
        #fpath='D:/software_git_repos/greenpol/telescope_control/configurations'
        os.chdir(fpath)
        folder='memory'
        if not os.path.exists(folder):#this is the first file being created for that time
            os.makedirs(folder)
        os.chdir(fpath+'/'+folder)

        if not os.path.exists(date):#this is the first file being created for that time
            os.makedirs(date)
        os.chdir(fpath+'/'+folder+'/'+date)
        

        fname=self.backup_r.get()

        if os.path.isfile(fname+'.txt')==True:
            print "LABEL EXISTS. Please change your label!"
        else:
            with open(fname+'.txt', 'w') as handle:
                pickle.dump(data,handle)

            print 'Recording a history config at '+ date+'/'+time +','+ 'naming: '+fname


    def read_txt(self):
        fname=self.backup_l.get()
        date=self.date_l.get()
        self.read(fname,date)
        
    def read(self,fname,date):
        fpath='D:/software_git_repos/greenpol/telescope_control/configurations/memory/'
        os.chdir(fpath+date)

        try:

            with open(fname+'.txt', 'r') as handle:
                data=pickle.loads(handle.read())
            print data['Move to Location']
            print 'Loading a history config of: '+ date +','+ 'naming: '+ fname

            ##Move Distance
            self.az.delete(0,'end')
            self.az.insert(END,data['Move Distance']['az'])
            self.el.delete(0,'end')
            self.el.insert(END,data['Move Distance']['el'])
            
            ##Move to Location
            key1,value1 = data['Move to Location'].items()[0]
            if key1 == 'el':
                key2='az'
            if key1 == 'dec':
                key2='ra'
            self.mtl1.config(text=key2)
            self.mtl2.config(text=key1)
            self.az2.delete(0,'end')
            self.az2.insert(END,data['Move to Location'][key2])
            self.el2.delete(0,'end')
            self.el2.insert(END,data['Move to Location'][key1])

            ##Az Scan
            self.tscan.delete(0,'end')
            self.tscan.insert(END,data['Az Scan']['Scan Time'])
            self.iterations.delete(0,'end')
            self.iterations.insert(END,data['Az Scan']['Iteration #'])
            self.deltaEl.delete(0,'end')
            self.deltaEl.insert(END,data['Az Scan']['El Step Size'])

            ##Linear Scan
            celestialcoord_lin=data['Linear Scan']['Celestial Object']
            if isinstance(celestialcoord_lin,str):
                self.cbody_lin.set(celestialcoord_lin)
                try:
                    self.cor1_lin.grid_forget()
                    self.cor2_lin.grid_forget()
                    self.cor1l_label.grid_forget()
                    self.cor2l_label.grid_forget()
                except:
                    pass
            if isinstance(celestialcoord_lin,list):
                self.cbody_lin.set(celestialcoord_lin[0])
                self.update_cbody_lin(celestialcoord_lin[0])
                self.cor1_lin.delete(0,'end')
                self.cor2_lin.delete(0,'end')
                self.cor1_lin.insert(END,celestialcoord_lin[1])
                self.cor2_lin.insert(END,celestialcoord_lin[2])
            self.numAzScans_lin.delete(0,'end')
            self.numAzScans_lin.insert(END,data['Linear Scan']['Az Scan #'])
            self.MinAz_lin.delete(0,'end')
            self.MinAz_lin.insert(END,data['Linear Scan']['Min Az'])
            self.MaxAz_lin.delete(0,'end')
            self.MaxAz_lin.insert(END,data['Linear Scan']['Max Az'])

            ##Horizontal Scan
            celestialcoord_hor=data['Horizontal Scan']['Celestial Object']
            if isinstance(celestialcoord_hor,str):
                self.cbody_hor.set(celestialcoord_hor)
                try:
                    self.cor1_hor.grid_forget()
                    self.cor2_hor.grid_forget()
                    self.cor1h_label.grid_forget()
                    self.cor2h_label.grid_forget()
                except:
                    pass
            if isinstance(celestialcoord_hor,list):
                self.cbody_hor.set(celestialcoord_hor[0])
                self.update_cbody_hor(celestialcoord_hor[0])
                self.cor1_hor.delete(0,'end')
                self.cor2_hor.delete(0,'end')
                self.cor1_hor.insert(END,celestialcoord_hor[1])
                self.cor2_hor.insert(END,celestialcoord_hor[2])
            self.numAzScans_hor.delete(0,'end')
            self.numAzScans_hor.insert(END,data['Horizontal Scan']['Az Scan #'])
            self.MinAz_hor.delete(0,'end')
            self.MinAz_hor.insert(END,data['Horizontal Scan']['Min Az'])
            self.MaxAz_hor.delete(0,'end')
            self.MaxAz_hor.insert(END,data['Horizontal Scan']['Max Az'])
            self.MinEl.delete(0,'end')
            self.MinEl.insert(END,data['Horizontal Scan']['Min El'])
            self.MaxEl.delete(0,'end')
            self.MaxEl.insert(END,data['Horizontal Scan']['Max El'])
            self.stepSize.delete(0,'end')
            self.stepSize.insert(END,data['Horizontal Scan']['Step Size'])



            ##plot
            self.date.delete(0,'end')
            self.date.insert(END,data['Plot']['Date'])
            self.beg.delete(0,'end')
            self.beg.insert(END,data['Plot']['From'])
            self.end.delete(0,'end')
            self.end.insert(END,data['Plot']['To'])

        except IOError:
            print 'No Labels Found'
        
    ####channel options for sci_data
    def update_ch(self,value):
        if value==self.choice1[3]:
            self.choice2=['all','ch0','ch1','ch2','ch3','ch4','ch5','ch6','ch7'
                          ,'ch8','ch9','ch10','ch11','ch12','ch13','ch14',
                          'ch15']
            self.bar2=StringVar()
            self.bar2.set('ch0')
            self.option2=OptionMenu(self.outputframe3,self.bar2,*self.choice2)
            self.option2.grid(row=2,column=1,sticky=W)
            self.choice3=['T','Q','U','PSD(T)','PSD(Q)','PSD(U)']
            self.bar3=StringVar()
            self.bar3.set('T')
            self.option3=OptionMenu(self.outputframe3,self.bar3,*self.choice3)
            self.option3.grid(row=1,column=1,sticky=W)

            self.l5.grid_forget()
            self.l6.grid_forget()
        else:
            try:
                self.option2.grid_forget()
                self.option3.grid_forget()
            except AttributeError:
                pass
            

    #tacking coordinate input        
    def update_cbody_lin(self,cbody):
        try:
            self.cor1_lin.grid_forget()
            self.cor2_lin.grid_forget()
            self.cor1l_label.grid_forget()
            self.cor2l_label.grid_forget()
        except:
            pass
        if cbody=='Sky-Coord':

            self.cor1_lin=Entry(self.inputframe_lin,width=5)
            self.cor1_lin.grid(row=1,column=3,sticky=W)
            self.cor2_lin=Entry(self.inputframe_lin,width=5)
            self.cor2_lin.grid(row=1,column=5,sticky=W)
            self.cor1l_label = Label(self.inputframe_lin, text='RA')
            self.cor1l_label.grid(row =1, column = 2, sticky=W)
            self.cor2l_label = Label(self.inputframe_lin, text='Dec')
            self.cor2l_label.grid(row =1, column = 4, sticky=W)


            
    def update_cbody_hor(self,cbody):
        try:
            self.cor1_hor.grid_forget()
            self.cor2_hor.grid_forget()
            self.cor1h_label.grid_forget()
            self.cor2h_label.grid_forget()
        except:
            pass
        if cbody=='Sky-Coord':
            self.cor1_hor=Entry(self.inputframe_hor,width=5)
            self.cor1_hor.grid(row=1,column=3,sticky=W)
            self.cor2_hor=Entry(self.inputframe_hor,width=5)
            self.cor2_hor.grid(row=1,column=5,sticky=W)
            self.cor1h_label = Label(self.inputframe_hor, text='RA')
            self.cor1h_label.grid(row =1, column = 2, sticky=W)
            self.cor2h_label = Label(self.inputframe_hor, text='Dec')
            self.cor2h_label.grid(row =1, column = 4, sticky=W)


    #keep this in case I want to compare encoder postion to galil position
    # i.e. moniter both at the same time
    def moniterGalil(self):

        t1 = time.time()

        while True:
            
            t2 = time.time()
            dt = t2 - t1
            
            if dt >= 2:
                Paz = (float(c2('TPX'))/ degtoctsAZ + offsetAz) % 360.
                Palt = (float(c2('TPY'))/ degtoctsEl + offsetEl) % 360.
                self.aztxtG.delete('1.0', END)
                self.aztxtG.insert('1.0', Paz)
                self.alttxtG.delete('1.0', END)
                self.alttxtG.insert('1.0', Palt)
                #this is currently asking galil for position, it needs to ask encoder

                #time.sleep(self.interval)
    def show_radec(self):
        self.lra=Label(self.outputframe2, text='ra')
        self.lra.grid(row=0, column=2, sticky=W)
        self.ratxt=Text(self.outputframe2, height=1, width=15)
        self.ratxt.grid(row=0,column=3)

        self.ldec=Label(self.outputframe2, text='dec')
        self.ldec.grid(row=1, column=2, sticky=W)
        self.dectxt=Text(self.outputframe2, height=1, width=15)
        self.dectxt.grid(row=1, column=3)
    def hide_radec(self):
        self.lra.grid_forget()
        self.ratxt.grid_forget()
        self.ldec.grid_forget()
        self.dectxt.grid_forget()
           
    
    def moniter(self):
    
        write_time = 60
        if len(sys.argv)==1: #this is the defualt no argument write time
            sys.argv.append(60) #this sets how long it takes to write a file
        #data = np.zeros(1000, dtype=[("first", np.int), ("second", np.int)])
        eye = gp.getData.Eyeball()
        Data = gp.datacollector()

        #gp.fileStruct(Data.getData()) 

        time_a = time.time()
        while True:
            #timer loop

            az, el, gpstime = gp.getAzEl(eye)
	    
	    #convert to radec
	    
	    ra, dec = planets.azel_to_radec(az, el, global_location)

            Data.add(az,el,gpstime)
            #print Data.getData()
            time_b = time.time()
            delta = time_b-time_a

            if (delta>=2):
                #print(rev,az,el)
                self.aztxt.delete('1.0', END)
                self.aztxt.insert('1.0', az)
                self.alttxt.delete('1.0', END)
                self.alttxt.insert('1.0', el)
		
		self.ratxt.delete('1.0', END)
		self.ratxt.insert('1.0', ra)
		self.dectxt.delete('1.0', END)
		self.dectxt.insert('1.0', dec)		

            if(delta>=int(write_time)): 
##                gp.fileStruct(Data.getData(), Data)
                time_a=time.time();
                print("file written")
                
        print("data collected at" + str(1.0/delta) +"HZ")
        
    def scanAz(self):

        tscan = self.tscan.get()
        if tscan == 'inf':
            tscan = np.inf
        else:
            tscan = float(tscan)
        iterations = int(self.iterations.get())
        deltaEl = float(self.deltaEl.get())

        thread = threading.Thread(target=scan.azScan, args=(tscan, iterations, deltaEl, c))
        thread.daemon = True
        thread.start()

        #scan.azScan(tscan, iterations, deltaEl, c)

    def linear(self):
        location = global_location
        cbody = self.cbody_lin.get()
        numAzScans = int(self.numAzScans_lin.get())
        MinAz = float(self.MinAz_lin.get())
        MaxAz = float(self.MaxAz_lin.get())

        if cbody == 'Sky-Coord':
            RA = self.cor1_lin.get()
            DEC = self.cor2_lin.get()
            cbody = [RA, DEC]

        thread = threading.Thread(target=scan.linearScan, args=(location, cbody, numAzScans, MinAz, MaxAz, c))
        thread.daemon = True
        thread.start()

        #scan.linearScan(location, cbody, numAzScans, MinAz, MaxAz, c)

    def horizontal(self):
        location = global_location
        cbody = self.cbody_hor.get()
        numAzScans = int(self.numAzScans_hor.get())
        MinAz = float(self.MinAz_hor.get())
        MaxAz = float(self.MaxAz_hor.get())
        MinEl = float(self.MinEl.get())
        MaxEl = float(self.MaxEl.get())
        stepSize = float(self.stepSize.get())

        if cbody == 'Sky-Coord':
            RA = self.cor1_lin.get()
            DEC = self.cor2_lin.get()
            cbody = [RA, DEC]        

        thread = threading.Thread(target=scan.horizontalScan, args=(location, cbody, numAzScans, MinAz, MaxAz, MinEl, MaxEl, stepSize, c))
        thread.daemon = True
        thread.start()

        #scan.horizontalScan(location, cbody, numAzScans, MinAz, MaxAz, MinEl, MaxEl, stepSize, c)


    def moveDist(self,x):
        if x=='+az':
            az=float(self.az.get())
            el=0
        if x=='-az':
            az=-float(self.az.get())
            el=0
        if x=='+el':
            az=0
            el=float(self.el.get())
        if x=='-el':
            az=0
            el=-float(self.el.get())
	
	thread = threading.Thread(target=moveto.distance, args=(az, el, c))
        thread.daemon = True
        thread.start()

        #moveto.distance(az, el, c)

    #moveto ra-dec displaying option
    def update_moveto(self):
        label=self.mtl1.cget('text')
        if label=='az':
            self.mtl1.grid_forget()
            self.mtl1=Label(self.inputframe2,text='ra')
            self.mtl1.grid(row=0,column=0,sticky=W)
            self.mtl2.grid_forget()
            self.mtl2=Label(self.inputframe2,text='dec')
            self.mtl2.grid(row=1,column=0,sticky=W)

        if label=='ra':
            self.mtl1.grid_forget()
            self.mtl1=Label(self.inputframe2,text='az')
            self.mtl1.grid(row=0,column=0,sticky=W)
            self.mtl2.grid_forget()
            self.mtl2=Label(self.inputframe2,text='el')
            self.mtl2.grid(row=1,column=0,sticky=W)


    def moveTo(self):
        #check if coordinates are az/el or ra/dec
        label=self.mtl1.cget('text')

        #if az/el just carry on
        if label=='az':
            az = float(self.az2.get())
            el = float(self.el2.get())

        # if ra/dec, convert to az/el
        if label=='ra':

            location = global_location

            ra = float(self.az2.get())
            dec = float(self.el2.get())
            az,el=planets.radec_to_azel(ra,dec, location)

        thread = threading.Thread(target=moveto.location, args=(az, el, c))
        thread.daemon = True
        thread.start()

    def plot(self):
        fpath='D:/software_git_repos/greenpol/telescope_control/'

        var1 = self.bar1.get()
        date = self.date.get()
        beg = self.beg.get()
        end = self.end.get()
    
        date = date.split('-')
        year = date[0]
        month = date[1]
        day = date[2]
        yrmoday=year+month+day

        time1 = beg.split('-')
        hour1 = str(time1[0])
        minute1 = str(time1[1])

        time2 = end.split('-')
        hour2 = str(time2[0])
        minute2 = str(time2[1])

        if var1 != 'sci_data':
            y=rt.get_h5_pointing(select_h5(fpath,yrmoday,hour1,minute1,
                                            hour2,minute2))[var1]
            t=rt.get_h5_pointing(select_h5(fpath,yrmoday,hour1,minute1,
                                            hour2,minute2))['gpstime']

            display_pointing = rt.pointing_plot(var1,y,t)

        else:
            var2 = self.bar2.get()
            var3 = self.bar3.get()
            psd=['PSD(T)','PSD(Q)','PSD(U)']
            parameter=['T','Q','U']
            if var2=='all' and var3 in parameter:
                rt.plotnow_all(fpath=fpath,yrmoday=yrmoday,chan=var2,var=var3,
                                     st_hour=hour1,st_minute=minute1,
                                     ed_hour=hour2,ed_minute=minute2)
            if var2=='all' and var3 in psd:
                indx=psd.index(var3)
                var3=parameter[indx]
                rt.plotnow_psd_all(fpath=fpath,yrmoday=yrmoday,chan=var2,var=var3,
                                     st_hour=hour1,st_minute=minute1,
                                     ed_hour=hour2,ed_minute=minute2)
            if var2 != 'all' and var3 in psd:
                indx=psd.index(var3)
                var3=parameter[indx]
                rt.plotnow_psd(fpath=fpath,yrmoday=yrmoday,chan=var2,var=var3,
                                     st_hour=hour1,st_minute=minute1,
                                     ed_hour=hour2,ed_minute=minute2)
               
            else:

                rt.plotnow(fpath=fpath,yrmoday=yrmoday,chan=var2,var=var3,
                                     st_hour=hour1,st_minute=minute1,
                                     ed_hour=hour2,ed_minute=minute2)
                
           # plt.plot(combdata[var1][var2][var3],label=ch+' '+ var3)
            

    #this does not currently work for horizontal scan, you have to keep pressing it
    
    def stop(self):
        print('stopping motion...')
        c('STX')
	c('STY')
    
    def motor(self):
        status = str(self.motorTxt.get('1.0',END))
        print len(status)
        #print status[0], ',', status[1], ',', status[2]
        on = status[:2]
        off = status[:3]

        #if its on, turn it off
        if on == 'ON':
            c('MO')
            self.motorTxt.delete('1.0', END)
            self.motorTxt.insert('1.0', 'OFF')
            print 'motor off'

        #if its off, turn it on
        elif off == 'OFF':
            c('SH')
            self.motorTxt.delete('1.0', END)
            self.motorTxt.insert('1.0', 'ON')  
            print 'motor on'

root = Tk()
root.title("Telescope Control")

b = interface(root)

root.mainloop()


g.GClose() #close connections


