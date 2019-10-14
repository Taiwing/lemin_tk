#!/usr/bin/env python3

from tkinter import *

class ToolTip(object):
    def __init__(self, widget, canvas=None):
        self.canvas = canvas
        self.widget = widget
        self.tipwindow = None
        self.x = self.y = 0

    # TODO: clean this, replace place_tip and place_shape_tip
    # by custom functions corresponding to each type of object
    # (ants, rooms, links, etc...)
    def place_tip(self):
        x1, y1, x2, y2 = self.widget.coords()
        self.tipwindow = Toplevel(self.widget)
        self.x = x1 + ((x2 - x1) / 2) 
        self.y = y1 + ((y2 - y1) / 2) 

    def place_shape_tip(self):
        x1, y1, x2, y2 = self.canvas.coords(self.widget)
        self.tipwindow = Toplevel(self.canvas)
        self.x = self.canvas.winfo_rootx() + x1
        self.y = self.canvas.winfo_rooty() + y1

    def showtip(self, text):
        self.text = text
        if self.tipwindow or not self.text:
            return
        if not self.canvas:
            self.place_tip()
        else:
            self.place_shape_tip()
        self.tipwindow.wm_overrideredirect(1)
        self.tipwindow.wm_geometry("+%d+%d" % (self.x, self.y))
        label = Label(self.tipwindow, text=self.text, justify=LEFT,\
        background="#ffffe0", relief=SOLID, borderwidth=1,\
        font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        if self.tipwindow:
            self.tipwindow.destroy()
        self.tipwindow = None

# works for widgets (canvas, buttons, etc...)
def CreateToolTip(widget, text):
    tooltip = ToolTip(widget)
    def enter(event):
        tooltip.showtip(text)
    def leave(event):
        tooltip.hidetip()
    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)

# works for shapes with tags (ovals, lines, etc...)
def CreateShapeToolTip(canvas, widget, text):
    tooltip = ToolTip(widget, canvas)
    def enter(event):
        tooltip.showtip(text)
    def leave(event):
        tooltip.hidetip()
    canvas.tag_bind(widget, "<Enter>", enter)
    canvas.tag_bind(widget, "<Leave>", leave)
