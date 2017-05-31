import scan
import scantest
import sys
sys.path.append('C:/Python27x86/lib/site-packages')
import gclib
from tkinter import *
from tkinter import ttk

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



class interface:

	#init gets called automatically
	def __init__(self, master):

		#nb = ttk.Notebook(master)

		#page1 = Frame(nb)

		topframe = Frame(master)
		topframe.pack()

		inputframe = Frame(master)
		inputframe.pack(side=TOP)

		buttonframe = Frame(master)
		buttonframe.pack(side=BOTTOM)

		self.title = Label(topframe, text = 'Az Scan')
		self.title.pack()

		self.l1 = Label(inputframe, text='scan time (seconds)')
		self.l1.grid(row = 0, column = 0, sticky=W)
		self.l2 = Label(inputframe, text='iteration #')
		self.l2.grid(row = 1, column = 0, sticky=W)
		self.l3 = Label(inputframe, text='El Step Size (deg)')
		self.l3.grid(row = 2, column = 0, sticky=W)
		self.l4 = Label(inputframe, text='starting az (deg)')
		self.l4.grid(row = 3, column = 0, sticky=W)
		self.l5 = Label(inputframe, text='starting el (deg)')
		self.l5.grid(row = 4, column = 0, sticky=W)

		#user input
		self.tscan = Entry(inputframe)
		self.tscan.insert(END, '5.0')
		self.tscan.grid(row = 0, column = 1)

		self.iterations = Entry(inputframe)
		self.iterations.insert(END, '2')
		self.iterations.grid(row = 1, column = 1)

		self.deltaEl = Entry(inputframe)
		self.deltaEl.insert(END, '90.0')
		self.deltaEl.grid(row = 2, column = 1)

		self.az0 = Entry(inputframe)
		self.az0.insert(END, '0.0')
		self.az0.grid(row = 3, column = 1)

		self.el0 = Entry(inputframe)
		self.el0.insert(END, '60.0')
		self.el0.grid(row = 4, column = 1)


		self.scan = Button(buttonframe, 
			text='Start Scan', 
			command=self.scanAz)
		self.scan.pack(side=LEFT)

		self.quitButton = Button(buttonframe, text='quit', command=master.quit)
		self.quitButton.pack(side=LEFT)

		#nb.add(page1, text='One')
    	#nb.add(page2, text='Two')

    	#nb.pack()


	def scanAz(self):

		tscan = float(self.tscan.get())
		iterations = int(self.iterations.get())
		deltaEl = float(self.deltaEl.get())
		az0 = float(self.az0.get())
		el0 = float(self.el0.get())

		scan.azScan(tscan, iterations, az0, el0, deltaEl, c)


root = Tk()
root.title("Telescope Control")

b = interface(root)

root.mainloop()

g.GClose() #close connections

