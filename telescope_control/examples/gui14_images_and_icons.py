from tkinter import *

root = Tk()

photo = PhotoImage(file='WMAP.png')
label = Label(root, image=photo)
label.pack()

root.mainloop()