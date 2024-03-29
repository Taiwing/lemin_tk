#!/usr/bin/env python3

from tkinter import *
from tooltip import *
from utils import *
from lemin_map import *
from lemin_grid import *
from map_compressor import *
from used_rooms import *

# update states
U_NONE = 0
U_WAIT = 1
U_REFRESH = 2
U_MOVE = 3
U_REDRAW = 4

# graphical constants
G_PRINT_GRID = True
G_PRINT_UNUSED_DEF = True
G_SIDE_MIN = 10
G_SCREEN_DIV = 2 # use half the screen by default
BACKGROUND_COLOR = "DodgerBlue3"
ROOM_COLOR = "blue"
START_ROOM_COLOR = "purple4"
END_ROOM_COLOR = "DarkGoldenrod1"
LINK_COLOR = "black"

class lemin_screen:
    def __init__(self, lwin, lmap, redrawf, movef, refreshf, waitf):
        # window data 
        self.lwin = lwin
        self.lwin.load_drawf(redrawf, movef, refreshf, waitf, None)
        # canvas data
        self.can = None
        self.canvas_w = 0
        self.canvas_h = 0
        self.redraw_w = 0
        self.redraw_h = 0
        self.side = 0
        self.orig_x = 0
        self.orig_y = 0
        # grid data
        # TODO: remove G_SIDE_MIN from grid parameters when config struct is on
        self.grid = lemin_grid(lmap, self.lwin.screen_width, self.lwin.screen_height, G_SIDE_MIN)
        # graphical objects
        self.lmap = lmap
        self.print_unused = G_PRINT_UNUSED_DEF
        self.roomn = len(lmap.rooms) # only printed rooms (all by default)

    def init_canvas(self):
        self.grid.get_min(self.lwin.screen_width,\
        self.lwin.screen_height, self.roomn)
        if self.grid.big_width * self.grid.big_height < self.roomn:
            # TODO: add a call to remove_unused here and check if it works
            # TODO: also replace the next elif by a if so that it always
            # TODO: compresses the map if needed
            if self.grid.big_width * self.grid.big_height < self.roomn:
                eprint("error: map too big for the screen")
                exit()
        elif self.grid.big_width < self.grid.width or self.grid.big_height < self.grid.height:
            compress_coordinates(self, compression="min")
        self.build_canvas()
        self.grid.w_comp_min = self.grid.w_comp
        self.grid.h_comp_min = self.grid.h_comp
        self.set_min_window()
        self.set_window_to_canvas()
        self.can.update()
        self.lwin.win.update()

    def build_canvas(self):
        self.canvas_w = self.lwin.screen_width / G_SCREEN_DIV 
        self.canvas_h = self.lwin.screen_height / G_SCREEN_DIV 
        if self.get_side_size():
            # if default window is not big enough
            self.canvas_w = (self.grid.width + 2) * G_SIDE_MIN
            self.canvas_h = (self.grid.height + 2) * G_SIDE_MIN
            self.get_side_size()
        self.can = Canvas(self.lwin.win, width=self.canvas_w, height=self.canvas_h,\
        bg=BACKGROUND_COLOR)
        self.lwin.updatef = self.can.update
        self.can.pack(side=TOP, fill=BOTH, expand=1)

    def set_min_window(self):
        self.lwin.win_w_min = (self.grid.width + 2) * G_SIDE_MIN
        self.lwin.win_h_min = (self.grid.height + 2) * G_SIDE_MIN
        self.lwin.win.minsize(self.lwin.win_w_min, self.lwin.win_h_min)

    def set_window_to_canvas(self):
        width = self.lwin.win.winfo_width()
        height = self.lwin.win.winfo_height()
        if width < self.canvas_w or height < self.canvas_h:
            self.lwin.win.geometry(str(int(self.canvas_w)) + "x" + str(int(self.canvas_h)))

    def get_side_size(self):
        self.side = min(self.canvas_w / (self.grid.width + 2),\
        self.canvas_h / (self.grid.height + 2))
        self.orig_x = (self.canvas_w - (self.grid.width * self.side)) / 2
        self.orig_y = (self.canvas_h - (self.grid.height * self.side)) / 2
        return 1 if self.side < G_SIDE_MIN else 0

    ## events handling of lemin_screen ##
    def init_events(self):
        self.can.bind("<Configure>", self.configure_handler)
        self.lwin.win.bind("+", self.plus_handler)
        self.lwin.win.bind("-", self.minus_handler)
        self.lwin.win.bind("*", self.star_handler)
        
    def configure_handler(self, event):
        self.lwin.stack.insert(0, self.scale_canvas)
        self.redraw_w = event.width
        self.redraw_h = event.height
    
    def plus_handler(self, event):
        self.lwin.stack.insert(0, self.compress_map)

    def minus_handler(self, event):
        self.lwin.stack.insert(0, self.uncompress_map)

    def star_handler(self, event):
        self.lwin.stack.insert(0, self.toggle_print_unused_rooms)

    def scale_canvas(self):
        self.lwin.update = U_REDRAW
        self.canvas_w = self.redraw_w
        self.canvas_h = self.redraw_h

    def compress_map(self):
        self.grid.w_comp = 5 if self.grid.w_comp < 5 else\
        self.grid.w_comp + 5 if self.grid.w_comp + 5 < 100 else 100
        self.grid.h_comp = 5 if self.grid.h_comp < 5 else\
        self.grid.h_comp + 5 if self.grid.h_comp + 5 < 100 else 100
        compress_coordinates(self, compression="cust",\
        w_comp=self.grid.w_comp, h_comp=self.grid.h_comp)
        self.set_min_window()
        self.lwin.update = U_REDRAW

    def uncompress_map(self):
        self.grid.w_comp = self.grid.w_comp_min if self.grid.w_comp - 5 < self.grid.w_comp_min\
        else self.grid.w_comp - 5
        self.grid.h_comp = self.grid.h_comp_min if self.grid.h_comp - 5 < self.grid.h_comp_min\
        else self.grid.h_comp - 5
        compress_coordinates(self, compression="cust",\
        w_comp=self.grid.w_comp, h_comp=self.grid.h_comp)
        self.set_min_window()
        self.lwin.update = U_REDRAW
    
    def toggle_print_unused_rooms(self):
        if self.print_unused == True:
            self.print_unused = False
            remove_unused_rooms(self)
        else:
            self.print_unused = True
            restore_unused_rooms(self)
            self.set_min_window()
        self.lwin.update = U_REDRAW

    ## drawing functions specific to lemin_screen ##
    def draw_map(self):
        self.delete_map()
        if G_PRINT_GRID:
            self.draw_grid()
        for r in self.lmap.rooms:
            self.draw_links(r)
        for r in self.lmap.rooms:
            self.draw_room(r)
        self.can.pack()

    def delete_map(self):
        self.delete_grid()
        for r in self.lmap.rooms:
            if self.lmap.rooms[r].shape != None:
                self.can.delete(self.lmap.rooms[r].shape)
            self.lmap.rooms[r].shape = None
        for r in self.lmap.unused_rooms:
            if self.lmap.unused_rooms[r].shape != None:
                self.can.delete(self.lmap.unused_rooms[r].shape)
            self.lmap.unused_rooms[r].shape = None
        for l in self.lmap.links:
            if self.lmap.links[l].shape != None:
                self.can.delete(self.lmap.links[l].shape)
            self.lmap.links[l].shape = None
    
    def draw_grid(self):
        self.delete_grid()
        for i in range(0, self.grid.width + 1):
            bar = self.can.create_line(self.orig_x + (self.side * i),\
            self.orig_y, self.orig_x + (self.side * i),\
            self.orig_y + (self.grid.height * self.side)) 
            self.grid.shapes.append(bar)
        for i in range(0, self.grid.height + 1):
            bar = self.can.create_line(self.orig_x,\
            self.orig_y + (self.side * i),\
            self.orig_x + (self.grid.width * self.side),\
            self.orig_y + (self.side * i))
            self.grid.shapes.append(bar)
        self.can.pack()
    
    def draw_links(self, r):
        for l in self.lmap.rooms[r].links:
            name = link_name(r, l)
            if l not in self.lmap.unused_rooms and self.lmap.links[name].shape == None:
                x1, y1, x2, y2 = self.link_coords(self.lmap.rooms[r].x,\
                self.lmap.rooms[r].y, self.lmap.rooms[l].x, self.lmap.rooms[l].y)
                link = self.can.create_line(x1, y1, x2, y2,\
                fill=LINK_COLOR, width=self.side/15)
                self.lmap.links[name].shape = link
    
    def draw_room(self, r):
        x1, y1, x2, y2 = self.room_coords(self.lmap.rooms[r].x,\
        self.lmap.rooms[r].y)
        color = START_ROOM_COLOR if self.lmap.start == r\
        else END_ROOM_COLOR if self.lmap.end == r else ROOM_COLOR
        room = self.can.create_oval(x1, y1, x2, y2, fill=color, tags=r)
        CreateShapeToolTip(self.can, room, r)
        self.lmap.rooms[r].shape = room
    
    def delete_grid(self):
        for bar in self.grid.shapes:
            self.can.delete(bar)
        self.grid.shapes.clear()

    def grid_to_graphical(self, g_x, g_y):
        return self.orig_x + (self.side * g_x) + self.side / 2,\
        self.orig_y + (self.side * g_y) + self.side / 2
    
    def room_coords(self, g_x, g_y):
        x, y = self.grid_to_graphical(g_x, g_y)
        return x - (self.side / 4), y - (self.side / 4),\
        x + (self.side / 4), y + (self.side / 4) 

    def link_coords(self, g_x1, g_y1, g_x2, g_y2):
        x1, y1 = self.grid_to_graphical(g_x1, g_y1)
        x2, y2 = self.grid_to_graphical(g_x2, g_y2)
        return x1, y1, x2, y2
