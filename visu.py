#!/usr/local/bin/python3

from tkinter import *

class vdata:
    def __init__(self):
        self.screen_w = 0
        self.screen_h = 0
        self.grid_w = 0
        self.grid_h = 0
        self.side = 0
        self.orig_x = 0
        self.orig_y = 0
        self.minx = 0
        self.miny = 0

    def init_values(self, win, col):
        self.screen_w = win.winfo_screenwidth() / 2
        self.screen_h = win.winfo_screenheight() / 2
        self.grid_w = abs(col.maxx - col.minx + 1)
        self.grid_h = abs(col.maxy - col.miny + 1)
        self.side = min(self.screen_w / (self.grid_w + 2),\
        self.screen_h / (self.grid_h + 2))
        self.orig_x = (self.screen_w - (self.grid_w * self.side)) / 2
        self.orig_y = (self.screen_h - (self.grid_h * self.side)) / 2
        self.minx = col.minx
        self.miny = col.miny
    
    # compute the coordinates to draw the rooms from grid coordinates
    def get_pos(self, g_x, g_y):
        return self.orig_x + (self.side * (g_x - self.minx)) + self.side / 4,\
        self.orig_y + (self.side * (g_y - self.miny)) + self.side / 4

def draw_grid(col, vda, can):
    for i in range(0, vda.grid_w + 1):
        can.create_line(vda.orig_x + (vda.side * i), vda.orig_y,\
        vda.orig_x + (vda.side * i), vda.orig_y + (vda.grid_h * vda.side)) 
    for i in range(0, vda.grid_h + 1):
        can.create_line(vda.orig_x, vda.orig_y + (vda.side * i),\
        vda.orig_x + (vda.grid_w * vda.side), vda.orig_y + (vda.side * i))
    can.pack()


def draw_rooms(col, vda, can):
    for room in col.rooms:
        x, y = vda.get_pos(col.rooms[room].x, col.rooms[room].y)
        can.create_oval(x, y, x + (vda.side / 2), y + (vda.side / 2),\
        fill="blue", outline="blue", width=2)

# TODO: this shit
def run_visu(col):
    win = Tk()
    vda = vdata()
    vda.init_values(win, col)
#    label = Label(win, text=str(screen_w) + "x" + str(screen_h) + "\n" + col.cprint())
 #   label.pack()

    # Background
    can = Canvas(win, width=vda.screen_w, height=vda.screen_h, bg="DodgerBlue3")
    can.pack(side=TOP, padx=5, pady=5)

    # Grid
    draw_grid(col, vda, can)

    # Rooms
    draw_rooms(col, vda, can)
    win.mainloop()
