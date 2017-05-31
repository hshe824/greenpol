from tkinter import *
import tkinter.messagebox

root = Tk()

#do this when elevation < 0
tkinter.messagebox.showinfo('Window Title', 'Monkeys are immortal')

answer = tkinter.messagebox.askquestion('Question 1', 'Do you like silly faces?')

if answer == 'yes':
	print('8--)>')
else:
	print('thats weird')

root.mainloop()