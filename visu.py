#!/usr/bin/env python3

from tkinter import *
from utils import *
from time import *

class vdata:
    def __init__(self):
        # grid data
        self.grid_w = 0
        self.grid_h = 0
        # screen data
        self.screen_w = 0
        self.screen_h = 0
        self.side = 0
        self.orig_x = 0
        self.orig_y = 0
        # screen
        self.win = Tk()
        self.can = None
        # shapes
        self.grid = []
        self.ants = []
        self.links = []
        self.rooms = {}
        # colors
        self.background_color = "DodgerBlue3"
        self.room_color = "blue"
        self.link_color = "black"
        self.ant_color = "red"
        # number of frames by ant movement (speed)
        self.framec = 100
        # print grid option
        self.print_grid = True

    def init_screen(self, col):
        self.grid_w = col.maxx + 1
        self.grid_h = col.maxy + 1
        self.screen_w = self.win.winfo_screenwidth() / 2
        self.screen_h = self.win.winfo_screenheight() / 2
        self.side = min(self.screen_w / (self.grid_w + 2),\
        self.screen_h / (self.grid_h + 2))
        if self.side < 10:
            eprint("error: map too big for the screen")
            exit()
        self.orig_x = (self.screen_w - (self.grid_w * self.side)) / 2
        self.orig_y = (self.screen_h - (self.grid_h * self.side)) / 2
        self.can = Canvas(self.win, width=self.screen_w, height=self.screen_h,\
        bg=self.background_color)
        self.can.pack(side=TOP, padx=5, pady=5)
    
    # compute the coordinates to draw the game from grid coordinates
    def grid_to_graphical(self, g_x, g_y):
        return self.orig_x + (self.side * g_x) + self.side / 2,\
        self.orig_y + (self.side * g_y) + self.side / 2

    def ant_coords(self, g_x, g_y):
        x, y = self.grid_to_graphical(g_x, g_y)
        return x - (self.side / 8), y - (self.side / 8),\
        x + (self.side / 8), y + (self.side / 8) 

    def room_coords(self, g_x, g_y):
        x, y = self.grid_to_graphical(g_x, g_y)
        return x - (self.side / 4), y - (self.side / 4),\
        x + (self.side / 4), y + (self.side / 4) 

    def link_coords(self, g_x1, g_y1, g_x2, g_y2):
        x1, y1 = self.grid_to_graphical(g_x1, g_y1)
        x2, y2 = self.grid_to_graphical(g_x2, g_y2)
        return x1, y1, x2, y2

    # grid
    def delete_grid(self):
        for bar in self.grid:
            self.can.delete(bar)
        self.grid.clear()

    def draw_grid(self):
        self.delete_grid()
        for i in range(0, self.grid_w + 1):
            bar = self.can.create_line(self.orig_x + (self.side * i),\
            self.orig_y, self.orig_x + (self.side * i),\
            self.orig_y + (self.grid_h * self.side)) 
            self.grid.append(bar)
        for i in range(0, self.grid_h + 1):
            bar = self.can.create_line(self.orig_x,\
            self.orig_y + (self.side * i),\
            self.orig_x + (self.grid_w * self.side),\
            self.orig_y + (self.side * i))
            self.grid.append(bar)
        self.can.pack()

    # delete the shapes of the game
    def delete_map(self):
        self.delete_grid()
        for r in self.rooms:
            self.can.delete(self.rooms[r])
        self.rooms.clear()
        for link in self.links:
            self.can.delete(link)
        self.links.clear()

    def delete_ants(self):
        for ant in self.ants:
            self.can.delete(ant)
        self.ants.clear()

    # draw the shapes of the game
    def draw_links(self, r, col):
        for l in col.rooms[r].links:
            if l not in self.rooms:
                x1, y1, x2, y2 = self.link_coords(col.rooms[r].x,\
                col.rooms[r].y, col.rooms[l].x, col.rooms[l].y)
                link = self.can.create_line(x1, y1, x2, y2,\
                fill=self.link_color, width=self.side/15)
                self.links.append(link)

    def draw_room(self, r, col):
            x1, y1, x2, y2 = self.room_coords(col.rooms[r].x, col.rooms[r].y)
            room = self.can.create_oval(x1, y1, x2, y2, fill=self.room_color)
            self.rooms[r] = room

    def draw_map(self, col):
        self.delete_map()
        if self.print_grid:
            self.draw_grid()
        for r in col.rooms:
            self.draw_links(r, col)
            self.draw_room(r, col)
        self.can.pack()

    # draw ants at current postition (according to col.turn)
    def draw_ants(self, col):
        self.delete_ants()
        for i in range(col.antn):
            r = col.game[col.turn][i]
            x1, y1, x2, y2 = self.ant_coords(col.rooms[r].x, col.rooms[r].y)
            ant = self.can.create_oval(x1, y1, x2, y2, fill=self.ant_color)
            self.ants.append(ant)
        self.can.pack()

    # animate the ants
    def get_steps(self, col):
        steps = []
        for i in range(col.antn):
            xy = self.ant_coords(col.rooms[col.game[col.turn][i]].x,\
            col.rooms[col.game[col.turn][i]].y)
            cur = self.can.coords(self.ants[i])
            ix = (xy[0] - cur[0]) / self.framec
            iy = (xy[1] - cur[1]) / self.framec
            steps.append([cur[0], cur[1], cur[2], cur[3], ix, iy])
        return steps

    def move_ants(self, col):
        # array of coordinates plus increment values
        steps = self.get_steps(col)
        for i in range(self.framec):
            for j in range(col.antn):
                if i < (self.framec - 1):
                    # move ant toward the next node
                    self.can.coords(self.ants[j],\
                    steps[j][0] + (steps[j][4] * i),\
                    steps[j][1] + (steps[j][5] * i),\
                    steps[j][2] + (steps[j][4] * i),\
                    steps[j][3] + (steps[j][5] * i))
                else:
                    # fix ant precisely on the node
                    xy = self.ant_coords(col.rooms[col.game[col.turn][j]].x,\
                    col.rooms[col.game[col.turn][j]].y)
                    self.can.coords(self.ants[j], xy[0], xy[1], xy[2], xy[3])
            self.can.pack()
            self.can.update()
        steps.clear()


def play_game(col, vda):
    col.turn = 1
    while col.turn < len(col.game):
        vda.move_ants(col)
        sleep(0.3)
        col.turn += 1

def run_visu(col):
    # init visual data
    vda = vdata()
    col.normalize_coords()
    vda.init_screen(col)

    # draw game 
    vda.draw_map(col)
    vda.draw_ants(col)
    vda.can.update()
    play_game(col, vda)
