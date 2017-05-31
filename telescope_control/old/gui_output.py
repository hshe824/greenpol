import scan
import moveto
import scantest
import config
import sys
sys.path.append('C:/Python27x86/lib/site-packages')
import gclib
from tkinter import ttk
from tkinter import *
import threading
import time

#make an instance of the gclib python class
g = gclib.py()
#connect to network
g.GOpen('10.1.2.245 --direct -s ALL')
#g.GOpen('COM1 --direct')
#used for galil commands
c = g.GCommand

c('AB') #abort motion and program
c('MO') #turn off all motors
c('SH') #servo on

degtoctsAZ = config.degtoctsAZ
degtoctsE = config.degtoctsE

class interface:

    def __init__(self, master): 

        outputframe = Frame(master)
        outputframe.pack()

        ####### output frame ##### 
        
        outputframe1 = Frame(outputframe)
        outputframe1.pack()

        outputframe2 = Frame(outputframe)
        outputframe2.pack()
        
        self.title = Label(outputframe1, text='Feedback')
        self.title.pack()

        self.laz = Label(outputframe2, text='az')
        self.laz.grid(row = 1, column = 0, sticky = E)

        self.aztxt = Text(outputframe2, height = 1, width = 15)
        self.aztxt.grid(row = 1, column = 1)

        self.lalt = Label(outputframe2, text='alt')
        self.lalt.grid(row = 2, column = 0, sticky = E)

        self.alttxt = Text(outputframe2, height = 1, width = 15)
        self.alttxt.grid(row = 2, column = 1)
        
        #thread stuff
        interval = 0.2
        self.interval = interval
        thread = threading.Thread(target=self.moniter, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start() 
        

    def moniter(self):

        Paz = (float(c('TPX')) % 1024000) / degtoctsAZ
        Palt = (float(c('TPY')) % 4096) / degtoctsE

        while True:

            self.aztxt.delete('1.0', END)
            self.aztxt.insert('1.0', Paz)
            self.alttxt.delete('1.0', END)
            self.alttxt.insert('1.0', Palt)
            tpx2 = c('TPX')
            print("TPX2", tpx2)
            tpy2 = c('TPY')
            print("TPY2", tpy2)
            Paz = (float(tpx2) % 1024000) / degtoctsAZ
            Palt = (float(tpy2) % 4096) / degtoctsE

            time.sleep(self.interval)  

       

root = Tk()
root.title("Telescope Control")

b = interface(root)

root.mainloop()

g.GClose() #close connections