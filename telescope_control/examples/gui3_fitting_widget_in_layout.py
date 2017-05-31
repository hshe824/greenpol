from tkinter import *

#creates a blank window
root = Tk()

one = Label(root, text="One", bg = "red", fg = "white")
one.pack()
two = Label(root, text="Two", bg = "green", fg = "black")
two.pack(fill=X) #button will grow with parent window
three = Label(root, text="Three", bg = "blue", fg = "white")
three.pack(side=LEFT, fill = Y)

#keeps the window running, rather than shutting down right away
root.mainloop()