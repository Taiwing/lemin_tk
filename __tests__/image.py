#!/usr/bin/env python3


import random
import math
from tkinter import Tk, Canvas, PhotoImage, mainloop

width = 1000
height = 600
window = Tk()
canvas = Canvas(window, width=width, height=height, bg="#000000")
canvas.pack(side="top")
canvas_bis = Canvas(window, width=width, height=height, bg="#fff")
canvas_bis.pack(side="bottom")
img = PhotoImage(width=width, height=height)
canvas.create_image((width//2, height//2), image=img, state="normal")

def center_and_invert(y, height):
    return int(height/2 - y)

def f(x):
    num_cycles = 4
    amplitude = 200
    return amplitude * math.sin(2 * math.pi * (num_cycles / width) * x)

def graph(f, x_range, height):
    for x in x_range:
        y = center_and_invert(f(x), height)
        img.put("#ffffff", (x, y))

graph(f, range(width), height)
mainloop()
