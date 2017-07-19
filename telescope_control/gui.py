#import scan
#import moveto
import config
#import connect
import os
import sys
sys.path.append('C:/Users/labuser/Desktop/python_temp')
sys.path.append('../')
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
'''
g = connect.g
c = g.GCommand
##
g2 = connect.g2
c2 = g2.GCommand

#offset between galil and beam
offsetAz = gp.galilAzOffset 
offsetEl = gp.galilElOffset
'''
degtoctsAZ = config.degtoctsAZ
degtoctsEl = config.degtoctsEl

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
        self.inputframe2 = Frame(page2)
        self.inputframe2.pack(side=TOP)

        buttonframe = Frame(page2)
        buttonframe.pack(side=BOTTOM)

        self.l1 = Label(self.inputframe2, text='Location')
        self.l1.grid(row = 0, column = 0, sticky=W)
        self.l2 = Label(self.inputframe2, text='Celestial Object')
        self.l2.grid(row = 1, column = 0, sticky=W)
        self.l3 = Label(self.inputframe2, text='Az Scan #')
        self.l3.grid(row = 2, column = 0, sticky=W)
        self.l4 = Label(self.inputframe2, text='Min Az')
        self.l4.grid(row = 3, column = 0, sticky=W)
        self.l5 = Label(self.inputframe2, text='Max AZ')
        self.l5.grid(row = 4, column = 0, sticky=W)

        #user input
        self.location_lin = Entry(self.inputframe2,width=10)
        self.location_lin.insert(END, 'UCSB')
        self.location_lin.grid(row = 0, column = 1,sticky=W)

        self.numAzScans_lin = Entry(self.inputframe2,width=10)
        self.numAzScans_lin.insert(END, '2')
        self.numAzScans_lin.grid(row = 2, column = 1,sticky=W)

        self.MinAz_lin = Entry(self.inputframe2,width=10)
        self.MinAz_lin.insert(END, '-10.0')
        self.MinAz_lin.grid(row = 3, column = 1,sticky=W)

        self.MaxAz_lin = Entry(self.inputframe2,width=10)
        self.MaxAz_lin.insert(END, '10.0')
        self.MaxAz_lin.grid(row = 4, column = 1,sticky=W)


        ##########linear tracking drop down#######
        self.planets = ['Sky-Coord','Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune']
        self.cbody_lin=StringVar(self.inputframe2)
        self.cbody_lin.set(self.planets[1])
        self.phouse=OptionMenu(self.inputframe2,self.cbody_lin,*self.planets,command=self.update_cbody_lin)
        self.phouse.grid(row = 1, column = 1,sticky=W)

        self.scan = Button(buttonframe, 
            text='Start Scan', 
            command=self.linear)
        self.scan.pack(side=LEFT)

        ###### horizontal scan ######
        page3 = Frame(nb2)
        self.inputframe3 = Frame(page3)
        self.inputframe3.pack(side=TOP)

        buttonframe = Frame(page3)
        buttonframe.pack(side=BOTTOM)

        self.l1 = Label(self.inputframe3, text='Location')
        self.l1.grid(row = 0, column = 0, sticky=W)
        self.l2 = Label(self.inputframe3, text='Celestial Object')
        self.l2.grid(row = 1, column = 0, sticky=W)
        self.l3 = Label(self.inputframe3, text='Az Scan #')
        self.l3.grid(row = 2, column = 0, sticky=W)
        self.l4 = Label(self.inputframe3, text='Min Az')
        self.l4.grid(row = 3, column = 0, sticky=W)
        self.l5 = Label(self.inputframe3, text='Max AZ')
        self.l5.grid(row = 4, column = 0, sticky=W)
        self.l6 = Label(self.inputframe3, text='Min El')
        self.l6.grid(row = 5, column = 0, sticky=W)
        self.l7 = Label(self.inputframe3, text='Max El')
        self.l7.grid(row = 6, column = 0, sticky=W)
        self.l8 = Label(self.inputframe3, text='Step Size')
        self.l8.grid(row = 7, column = 0, sticky=W)

        #user input
        self.location_hor = Entry(self.inputframe3,width=10)
        self.location_hor.insert(END, 'UCSB')
        self.location_hor.grid(row = 0, column = 1,sticky=W)

        self.numAzScans_hor = Entry(self.inputframe3,width=10)
        self.numAzScans_hor.insert(END, '2')
        self.numAzScans_hor.grid(row = 2, column = 1,sticky=W)

        self.MinAz_hor = Entry(self.inputframe3,width=10)
        self.MinAz_hor.insert(END, '-10.0')
        self.MinAz_hor.grid(row = 3, column = 1,sticky=W)

        self.MaxAz_hor = Entry(self.inputframe3,width=10)
        self.MaxAz_hor.insert(END, '10.0')
        self.MaxAz_hor.grid(row = 4, column = 1,sticky=W)

        self.MinEl = Entry(self.inputframe3,width=10)
        self.MinEl.insert(END, '-10.0')
        self.MinEl.grid(row = 5, column = 1,sticky=W)

        self.MaxEl = Entry(self.inputframe3,width=10)
        self.MaxEl.insert(END, '10.0')
        self.MaxEl.grid(row = 6, column = 1,sticky=W)

        self.stepSize = Entry(self.inputframe3,width=10)
        self.stepSize.insert(END, '10.0')
        self.stepSize.grid(row = 7, column = 1,sticky=W)


        
        ##########horizontal tracking drop down#######
        self.planets = ['Sky-Coord', 'Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune']
        self.cbody_hor=StringVar(self.inputframe3)
        self.cbody_hor.set(self.planets[1])
        self.phouse=OptionMenu(self.inputframe3,self.cbody_hor,*self.planets,command=self.update_cbody_hor)  
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
        self.l2.grid(row = 1, column = 0, sticky=W)

        #user input
        self.az = Entry(inputframe)
        self.az.insert(END, '0.0')
        self.az.grid(row = 0, column = 1)

        self.el = Entry(inputframe)
        self.el.insert(END, '0.0')
        self.el.grid(row = 1, column = 1)

        self.scan = Button(buttonframe, 
            text='Start Move', command=self.moveDist)
        self.scan.pack(side=LEFT)

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

        #self.convert=Button(self.buttonframe2,
        #                    text='radec/azel',command=self.update_moveto)
        #self.convert.pack(side=RIGHT)

        ####### notebook layout #########
        nb.add(movePage, text='Move')
        nb.add(page1, text='Az Scan')
        nb.add(nb2, text='Track')
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
        
        #thread = threading.Thread(target=self.moniterGalil, args=())
        #thread.daemon = True                            # Daemonize thread
        #thread.start() 

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

        ###########Record and Load Configuration###########

        self.outputframe4 = Frame(outputframe)
        self.outputframe4.pack()
        self.backup_l = Entry(self.outputframe4, width=20)
        self.backup_l.grid(row=1,column=2,sticky=W)
        self.backup_l.insert(END,'Target Label')
        self.date_l=Entry(self.outputframe4, width=20)
        self.date_l.grid(row=1,column=1,sticky=W)
        self.date_l.insert(END,'2017-06-28')
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


##                self.var.delete(0,'end')
##                self.var.insert(END,self.choices[i])

    def write_txt(self):
        data={'Move Distance':{'az':self.az.get(),'el':self.el.get()},
                   'Move to Location':{'az':self.az2.get(),'el':self.el2.get()},
                   'Az Scan':{'Scan Time':self.tscan.get(),'Iteration #':
                              self.iterations.get(),'El Step Size':self.deltaEl.get()},
                   'Linear Scan':{'Location':self.location_lin.get(),
                                  'Celestial Object':self.cbody_lin.get(),
                                  'Az Scan #':self.numAzScans_lin.get(),
                                  'Min Az':self.MinAz_lin.get(),
                                  'Max Az':self.MaxAz_lin.get()},
                   'Horizontal Scan':{'Location':self.location_hor.get(),
                                      'Celestial Object':self.cbody_hor.get(),
                                      'Az Scan #':self.numAzScans_hor.get(),
                                      'Min Az':self.MinAz_hor.get(),
                                      'Max Az':self.MaxAz_hor.get(),
                                      'Min El':self.MinEl.get(),
                                      'Max El':self.MaxEl.get(),
                                      'Step Size':self.stepSize.get()}}
        date = strftime("%Y-%m-%d")
        time=strftime("%H-%M-%S")
        fpath='D:/software_git_repos/greenpol/telescope_control/configurations'
        os.chdir(fpath)
        fd="gui_config-"+date
        if not os.path.exists(fd):#this is the first file being created for that time
            os.makedirs(fd)
        os.chdir(fpath+'/'+fd)

        fname=self.backup_r.get()

        if os.path.isfile(fname+'.txt')==True:
            print "LABEL EXISTS. Please change your label!"
        else:
            with open(fname+'.txt', 'w') as handle:
                pickle.dump(data,handle)

            print 'Recording a history config at '+ date+'/'+time +','+ 'naming: '+fname


    def read_txt(self):
        fname=self.backup_l.get()
        fpath='c:/Users/shulin/greenpol/'
        date=self.date_l.get()
        os.chdir(fpath+'/'+date)

        with open(fname+'.txt', 'r') as handle:
            data=pickle.loads(handle.read())
        print 'Loading a history config of: '+ date +','+ 'naming: '+ fname

        ##Move Distance
        self.az.delete(0,'end')
        self.az.insert(END,data['Move Distance']['az'])
        self.el.delete(0,'end')
        self.el.insert(END,data['Move Distance']['el'])
        
        ##Move to Location
        self.az2.delete(0,'end')
        self.az2.insert(END,data['Move to Location']['az'])
        self.el2.delete(0,'end')
        self.el2.insert(END,data['Move to Location']['el'])

        ##Az Scan
        self.tscan.delete(0,'end')
        self.tscan.insert(END,data['Az Scan']['Scan Time'])
        self.iterations.delete(0,'end')
        self.iterations.insert(END,data['Az Scan']['Iteration #'])
        self.deltaEl.delete(0,'end')
        self.deltaEl.insert(END,data['Az Scan']['El Step Size'])

        ##Linear Scan
        self.location_lin.delete(0,'end')
        self.location_lin.insert(END,data['Linear Scan']['Location'])
        self.cbody_lin.set(data['Linear Scan']['Celestial Object'])
        self.numAzScans_lin.delete(0,'end')
        self.numAzScans_lin.insert(END,data['Linear Scan']['Az Scan #'])
        self.MinAz_lin.delete(0,'end')
        self.MinAz_lin.insert(END,data['Linear Scan']['Min Az'])
        self.MaxAz_lin.delete(0,'end')
        self.MaxAz_lin.insert(END,data['Linear Scan']['Max Az'])

        ##Horizontal Scan
        self.location_hor.delete(0,'end')
        self.location_hor.insert(END,data['Horizontal Scan']['Location'])
        self.cbody_hor.set(data['Horizontal Scan']['Celestial Object'])
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
            self.option2.grid_forget()
            self.option3.grid_forget()
        

    #tacking coordinate input        
    def update_cbody_lin(self,cbody):
        if cbody=='Sky-Coord':

            self.cor1_lin=Entry(self.inputframe2,width=5)
            self.cor1_lin.grid(row=1,column=3,sticky=W)
            self.cor2_lin=Entry(self.inputframe2,width=5)
            self.cor2_lin.grid(row=1,column=5,sticky=W)
            self.cor1l_label = Label(self.inputframe2, text='RA')
            self.cor1l_label.grid(row =1, column = 2, sticky=W)
            self.cor2l_label = Label(self.inputframe2, text='Dec')
            self.cor2l_label.grid(row =1, column = 4, sticky=W)

        else:
            self.cor1_lin.grid_forget()
            self.cor2_lin.grid_forget()
            self.cor1l_label.grid_forget()
            self.cor2l_label.grid_forget()

            
    def update_cbody_hor(self,cbody):
        if cbody=='Sky-Coord':
            self.cor1_hor=Entry(self.inputframe3,width=5)
            self.cor1_hor.grid(row=1,column=3,sticky=W)
            self.cor2_hor=Entry(self.inputframe3,width=5)
            self.cor2_hor.grid(row=1,column=5,sticky=W)
            self.cor1h_label = Label(self.inputframe3, text='RA')
            self.cor1h_label.grid(row =1, column = 2, sticky=W)
            self.cor2h_label = Label(self.inputframe3, text='Dec')
            self.cor2h_label.grid(row =1, column = 4, sticky=W)
        else:
            self.cor1_hor.grid_forget()
            self.cor2_hor.grid_forget()
            self.cor1h_label.grid_forget()
            self.cor2h_label.grid_forget()  


    #keep this in case I want to compare encoder postion to galil position
    # i.e. moniter both at the same time
    def moniterGalil(self):

        t1 = time.time()

        while True:
            
            t2 = time.time()
            dt = t2 - t1
            
            if dt >= 2:
                Paz = (((float(c2('TPX')) % 1024000) / degtoctsAZ) + offsetAz) % 360
                Palt = (((float(c2('TPY')) % 4096) / degtoctsEl) + offsetEl) % 360
                self.aztxtG.delete('1.0', END)
                self.aztxtG.insert('1.0', Paz)
                self.alttxtG.delete('1.0', END)
                self.alttxtG.insert('1.0', Palt)
                #this is currently asking galil for position, it needs to ask encoder

                #time.sleep(self.interval) 
           
    
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

            if(delta>=int(write_time)): 
                gp.fileStruct(Data.getData(), Data)
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
        location = self.location_lin.get()
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
        location = self.location_hor.get()
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

    def moveDist(self):
        az = float(self.az.get())
        el = float(self.el.get())

        thread = threading.Thread(target=moveto.distance, args=(az, el, c))
        thread.daemon = True
        thread.start()

        #moveto.distance(az, el, c)


    def moveTo(self):
        az = float(self.az2.get())
        el = float(self.el2.get())

        thread = threading.Thread(target=moveto.location, args=(az, el, c))
        thread.daemon = True
        thread.start()

        #moveto.location(az, el, c)


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
	    print'plotting science data'

            display_pointing = rt.pointing_plot(var1,y,t)

        else:
            var2 = self.bar2.get()
            var3 = self.bar3.get()
            psd=['PSD(T)','PSD(Q)','PSD(U)']
            parameter=['T','Q','U']
            if var2=='all' and var3 in parameter:
		print'plotting all in parameter'
                rt.plotnow_all(fpath=fpath,yrmoday=yrmoday,chan=var2,var=var3,
                                     st_hour=hour1,st_minute=minute1,
                                     ed_hour=hour2,ed_minute=minute2)\
		
            if var2=='all' and var3 in psd:
                indx=psd.index(var3)
                var3=parameter[indx]
		print'plotting all in psd'
                rt.plotnow_psd_all(fpath=fpath,yrmoday=yrmoday,chan=var2,var=var3,
                                     st_hour=hour1,st_minute=minute1,
                                     ed_hour=hour2,ed_minute=minute2)
            if var2 != 'all' and var3 in psd:
                indx=psd.index(var3)
                var3=parameter[indx]
		print'plotting channel in psd'
                rt.plotnow_psd(fpath=fpath,yrmoday=yrmoday,chan=var2,var=var3,
                                     st_hour=hour1,st_minute=minute1,
                                     ed_hour=hour2,ed_minute=minute2)
		
               
            else:
		print'plotting channel in parameter'

                rt.plotnow(fpath=fpath,yrmoday=yrmoday,chan=var2,var=var3,
                                     st_hour=hour1,st_minute=minute1,
                                     ed_hour=hour2,ed_minute=minute2)
		
                
           # plt.plot(combdata[var1][var2][var3],label=ch+' '+ var3)
            

    #this does not currently work for horizontal scan, you have to keep pressing it
    
    def stop(self):
        print('stopping motion...')
        c('ST')
    
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
