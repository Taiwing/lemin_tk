#!/usr/bin/env python3

from tkinter import *
from utils import *
from time import *

class vdata:
    def __init__(self):
        self.screen_w = 0
        self.screen_h = 0
        self.grid_w = 0
        self.grid_h = 0
        self.side = 0
        self.orig_x = 0
        self.orig_y = 0

    # build grid
    def init_values(self, win, col):
        self.screen_w = win.winfo_screenwidth() / 2
        self.screen_h = win.winfo_screenheight() / 2
        self.grid_w = col.maxx + 1
        self.grid_h = col.maxy + 1
        self.side = min(self.screen_w / (self.grid_w + 2),\
        self.screen_h / (self.grid_h + 2))
        if self.side < 10:
            eprint("error: map too big for the screen")
            exit()
        self.orig_x = (self.screen_w - (self.grid_w * self.side)) / 2
        self.orig_y = (self.screen_h - (self.grid_h * self.side)) / 2
    
    # compute the coordinates to draw the rooms from grid coordinates
    def get_pos(self, g_x, g_y):
        return self.orig_x + (self.side * g_x) + self.side / 2,\
        self.orig_y + (self.side * g_y) + self.side / 2


def draw_grid(col, vda, can):
    for i in range(0, vda.grid_w + 1):
        can.create_line(vda.orig_x + (vda.side * i), vda.orig_y,\
        vda.orig_x + (vda.side * i), vda.orig_y + (vda.grid_h * vda.side)) 
    for i in range(0, vda.grid_h + 1):
        can.create_line(vda.orig_x, vda.orig_y + (vda.side * i),\
        vda.orig_x + (vda.grid_w * vda.side), vda.orig_y + (vda.side * i))
    can.pack()

def draw_room(vda, can, x, y):
        can.create_oval(x - (vda.side / 4), y - (vda.side / 4),\
        x + (vda.side / 4), y + (vda.side / 4), fill="blue")

def draw_links(r, col, vda, can, x, y):
    for l in col.rooms[r].links:
        if col.rooms[l].drawn == 0:
            lx, ly = vda.get_pos(col.rooms[l].x, col.rooms[l].y)
            can.create_line(x, y, lx, ly, fill="black", width=vda.side/15)

def draw_map(col, vda, can):
    for r in col.rooms:
        x, y = vda.get_pos(col.rooms[r].x, col.rooms[r].y)
        draw_links(r, col, vda, can, x, y)
        draw_room(vda, can, x, y)
        col.rooms[r].drawn = 1
    can.pack()

def init_ants(col, vda, can):
    for i in range(col.antn):
        x, y = vda.get_pos(col.rooms[col.start].x, col.rooms[col.start].y)
        ant = can.create_oval(x - (vda.side / 8), y - (vda.side / 8),\
        x + (vda.side / 8), y + (vda.side / 8), fill="red")
        col.ants.append(ant)
    can.pack()

def move_ants(col, vda, can):
    # array of coordinates plus increment values
    xy = []
    framec = 100
    for i in range(col.antn):
        x1, y1 = vda.get_pos(col.rooms[col.game[col.turn][i]].x,\
        col.rooms[col.game[col.turn][i]].y)
        x1 -= (vda.side / 8)
        y1 -= (vda.side / 8)
        cur = can.coords(col.ants[i])
        ix = (x1 - cur[0]) / framec
        iy = (y1 - cur[1]) / framec
        xy.append([cur[0], cur[1], cur[2], cur[3], ix, iy])
    for i in range(framec):
        for j in range(col.antn):
            if i < (framec - 1):
                can.coords(col.ants[j], xy[j][0] + (xy[j][4] * i),\
                xy[j][1] + (xy[j][5] * i), xy[j][2] + (xy[j][4] * i),\
                xy[j][3] + (xy[j][5] * i))
            else:
                x1, y1 = vda.get_pos(col.rooms[col.game[col.turn][j]].x,\
                col.rooms[col.game[col.turn][j]].y)
                x2 = x1 + (vda.side / 8)
                y2 = y1 + (vda.side / 8)
                x1 -= (vda.side / 8)
                y1 -= (vda.side / 8)
                can.coords(col.ants[j], x1, y1, x2, y2)
        can.pack()
        can.update()

def play_game(col, vda, can):
    col.turn = 1
    while col.turn < len(col.game):
        move_ants(col, vda, can)
        sleep(0.3)
        col.turn += 1

def run_visu(col):
    win = Tk()
    vda = vdata()
    col.normalize_coords()
    vda.init_values(win, col)

    # Background
    can = Canvas(win, width=vda.screen_w, height=vda.screen_h, bg="DodgerBlue3")
    can.pack(side=TOP, padx=5, pady=5)

    # Grid
#    draw_grid(col, vda, can)

    # Map
    draw_map(col, vda, can)

    init_ants(col, vda, can)
    can.update()
    play_game(col, vda, can)
   # win.mainloop()
