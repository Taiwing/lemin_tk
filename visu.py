#!/usr/bin/env python3

from tkinter import *
from tooltip import *
from utils import *
from time import *

class vdata:
    def __init__(self, col):
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
        self.start_room_color = "purple4"
        self.end_room_color = "DarkGoldenrod1"
        self.link_color = "black"
        self.ant_color = "red"
        # number of frames by ant movement (speed)
        self.framec = 100
        # current coordinates and x,y increments for each ant
        self.steps = []
        self.step = 0
        # print grid option
        self.print_grid = True
        # copy of colony class for convenience
        self.col = col

    def scale_canvas(self, event):
        self.can.pack(side=TOP, fill=BOTH, expand=1)
        if self.build_canvas_grid(event.width, event.height):
            eprint("error: map too big for the screen")
            exit()
        self.draw_map()
        # this shit is called before the game is even launched, whyyyy ?
        self.draw_ants(turn=self.col.turn - 1 if self.col.turn > 0 else 0)
        if self.col.turn < len(self.col.game):
            self.get_steps()
            self.draw_step()
        self.can.update()

    def build_canvas_grid(self, width, height):
        self.screen_w = width
        self.screen_h = height
        self.side = min(self.screen_w / (self.grid_w + 2),\
        self.screen_h / (self.grid_h + 2))
        self.orig_x = (self.screen_w - (self.grid_w * self.side)) / 2
        self.orig_y = (self.screen_h - (self.grid_h * self.side)) / 2
        if self.side < 10:
            return 1
        else:
            return 0

    def init_screen(self):
        self.grid_w = self.col.maxx + 1
        self.grid_h = self.col.maxy + 1
        self.screen_w = self.win.winfo_screenwidth() / 2
        self.screen_h = self.win.winfo_screenheight() / 2
        # try to resize the grid to a minimum if it does not fit the screen
        if self.build_canvas_grid(self.screen_w, self.screen_h):
            self.screen_w = (self.grid_w + 2) * 10
            self.screen_h = (self.grid_h + 2) * 10
            self.build_canvas_grid(self.screen_w, self.screen_h)
            if self.screen_w > self.win.winfo_screenwidth()\
            or self.screen_h > self.win.winfo_screenheight():
                eprint("error: map too big for the screen")
                exit()
        self.can = Canvas(self.win, width=self.screen_w, height=self.screen_h,\
        bg=self.background_color)
        self.can.pack(side=TOP, fill=BOTH, expand=1)
        self.can.bind("<Configure>", self.scale_canvas)
    
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
    def draw_links(self, r):
        for l in self.col.rooms[r].links:
            if l not in self.rooms:
                x1, y1, x2, y2 = self.link_coords(self.col.rooms[r].x,\
                self.col.rooms[r].y, self.col.rooms[l].x, self.col.rooms[l].y)
                link = self.can.create_line(x1, y1, x2, y2,\
                fill=self.link_color, width=self.side/15)
                self.links.append(link)

    def draw_room(self, r):
        x1, y1, x2, y2 = self.room_coords(self.col.rooms[r].x, self.col.rooms[r].y)
        color = self.start_room_color if self.col.start == r\
        else self.end_room_color if self.col.end == r else self.room_color
        room = self.can.create_oval(x1, y1, x2, y2, fill=color, tags=r)
        CreateShapeToolTip(self.can, room, r)
        self.rooms[r] = room

    def draw_map(self):
        self.delete_map()
        if self.print_grid:
            self.draw_grid()
        for r in self.col.rooms:
            self.draw_links(r)
            self.draw_room(r)
        self.can.pack()

    # draw ants at current postition (according to self.col.turn)
    def draw_ants(self, turn=0):
        self.delete_ants()
        for i in range(self.col.antn):
            r = self.col.game[turn][i]
            x1, y1, x2, y2 = self.ant_coords(self.col.rooms[r].x, self.col.rooms[r].y)
            ant = self.can.create_oval(x1, y1, x2, y2, fill=self.ant_color)
            self.ants.append(ant)
        self.can.pack()

    # animate the ants
    def get_steps(self):
        self.steps.clear()
        for i in range(self.col.antn):
            xy = self.ant_coords(self.col.rooms[self.col.game[self.col.turn][i]].x,\
            self.col.rooms[self.col.game[self.col.turn][i]].y)
            cur = self.can.coords(self.ants[i])
            ix = (xy[0] - cur[0]) / self.framec
            iy = (xy[1] - cur[1]) / self.framec
            self.steps.append([cur[0], cur[1], cur[2], cur[3], ix, iy])

    def draw_step(self):
        for j in range(self.col.antn):
            # move ant one frame toward the next node
            self.can.coords(self.ants[j],\
            self.steps[j][0] + (self.steps[j][4] * self.step),\
            self.steps[j][1] + (self.steps[j][5] * self.step),\
            self.steps[j][2] + (self.steps[j][4] * self.step),\
            self.steps[j][3] + (self.steps[j][5] * self.step))

    def move_ants(self):
        # array of coordinates plus increment values
        self.get_steps()
        self.step = 0
        while self.step <= self.framec:
            self.draw_step()
            self.can.update()
            self.step += 1
        for i in range(self.col.antn):
            # fix ant precisely on the node
            xy = self.ant_coords(self.col.rooms[self.col.game[self.col.turn][i]].x,\
            self.col.rooms[self.col.game[self.col.turn][i]].y)
            self.can.coords(self.ants[i], xy[0], xy[1], xy[2], xy[3])

def play_game(col, vda):
    if col.turn < len(col.game):
        vda.move_ants()
        col.turn += 1
        vda.win.after(300, play_game, col, vda)

def run_visu(col):
    # init visual data
    vda = vdata(col)
    col.normalize_coords()
    vda.init_screen()

    # draw game 
    vda.draw_map()
    vda.draw_ants()
    vda.can.update()

    # main loop
    col.turn = 1
    vda.win.after(300, play_game, col, vda)
    vda.win.mainloop()
