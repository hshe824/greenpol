from tkinter import *

#creates a blank window
root = Tk()

#put text on a screen
theLabel = Label(root, text='easy')

#where to put the window, pack just puts it somewhere
theLabel.pack()

#keeps the window running, rather than shutting down right away
root.mainloop()