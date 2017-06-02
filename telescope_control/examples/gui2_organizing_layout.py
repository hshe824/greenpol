from tkinter import *

#creates a blank window
root = Tk()

#create invisible container in our window..
topFrame = Frame(root)
#put it somewhere
topFrame.pack()
bottomFrame = Frame(root)
#put it on the bottom
bottomFrame.pack(side=BOTTOM)

#make a button, (where to put it, what do you want in the button)
button1 = Button(topFrame, text='Button 1', fg='red')
button2 = Button(topFrame, text='Button 2', fg='blue')
button3 = Button(topFrame, text='Button 3', fg='green')
button4 = Button(bottomFrame, text='Button 4', fg='purple')

#display them on your screen
button1.pack(side=LEFT) # defaults to on top of each other
button2.pack(side=LEFT) #can change that by passing argument to pack
button3.pack(side=LEFT) #places as far left as possible
button4.pack(side=BOTTOM)

#keeps the window running, rather than shutting down right away
root.mainloop()