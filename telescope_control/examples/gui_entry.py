from tkinter import *

root = Tk()


label1 = Label( root, text="Month(MM)")
E1 = Entry(root, bd =5)

label2 = Label( root, text="Day(DD)")
E2 = Entry(root, bd =5)

label3 = Label( root, text="Year(YYYY)")
E3 = Entry(root, bd =5)

def getDate():
    print(E1.get())
    print(E2.get())
    print(E3.get())

submit = Button(root, text ="Submit", command = getDate)

label1.pack()
E1.pack()
label2.pack()
E2.pack()
label3.pack()
E3.pack()
submit.pack(side =BOTTOM) 
root.mainloop()