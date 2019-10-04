#!/usr/bin/env python3

from tkinter import *
from random import randint

A=Tk()
B=Canvas(A)
B.place(x=0,y=0,height=256,width=256)
for a in range(256):
    a_color = "#%02x" % a
    for b in range(256):
        color = a_color + "%02x%02x" % (b, randint(0, 255))
        B.create_line(a,b,a+1,b+1,fill=color)
A.geometry("256x256")
mainloop()
