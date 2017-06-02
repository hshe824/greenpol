from tkinter import *

#creates a blank window
root = Tk()

label_1 = Label(root, text='name')
label_2 = Label(root, text='password')

#user input
entry_1 = Entry(root)
entry_2 = Entry(root)

#where to put it
label_1.grid(row=0, sticky=E) #sticky: N,S,W,E, alignment
label_2.grid(row=1, sticky=E)

entry_1.grid(row=0, column=1)
entry_2.grid(row=1, column=1)

cb = Checkbutton(root, text='Keep me logged in')

cb.grid(columnspan=2)

#keeps the window running, rather than shutting down right away
root.mainloop()