from tkinter import *

#creates a blank window
root = Tk()
'''
def printName():
	print('hello Im batman')

button_1 = Button(root, text='print name', command=printName)
button_1.pack()
'''

#method 2
def printName(event):
	print('hello Im batman')

button_1 = Button(root, text='print my name')

#button-1 corresponds to left mouse click
button_1.bind('<Button-1>', printName)
button_1.pack()

#keeps the window running, rather than shutting down right away
root.mainloop()