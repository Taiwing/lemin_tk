#!/usr/local/bin/python3

from tkinter import *

# TODO: this shit
def run_visu(col):
    win = Tk()
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
#    label = Label(win, text=str(screen_w) + "x" + str(screen_h) + "\n" + col.cprint())
 #   label.pack()
    can = Canvas(win, width=screen_w/2, height=screen_h/2, bg="DodgerBlue3")
    can.pack(side=TOP, padx=5, pady=5)
    win.mainloop()
