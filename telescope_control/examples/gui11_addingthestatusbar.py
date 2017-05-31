from tkinter import *

def doNothing():
	print('blah blah blah')

root = Tk()

#main menu
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

#toolbar
toolbar = Frame(root, bg='Blue')

insertButt = Button(toolbar, text='Insert Image', command=doNothing)
insertButt.pack(side=LEFT, padx=2, pady=2)
printButt = Button(toolbar, text='print', command=doNothing)
printButt.pack(side=LEFT, padx=2, pady=2)

toolbar.pack(side=TOP, fill=X)

#status bar
status = Label(root, text='Preparing to do nothing...',
	bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)


root.mainloop()