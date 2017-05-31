from tkinter import *

def doNothing():
	print('blah blah blah')

root = Tk()

menu = Menu(root)
root.config(menu=menu)

subMenu = Menu(menu)
menu.add_cascade(label='File', menu=subMenu)

subMenu.add_command(label='New Project...', 
	command=doNothing)
subMenu.add_command(label='New...', 
	command=doNothing)
subMenu.add_separator()
subMenu.add_command(label='exit', command=doNothing)

editMenu = Menu(menu)
menu.add_cascade(label='Edit', menu=editMenu)
editMenu.add_command(label = 'redo', command=doNothing)

root.mainloop()