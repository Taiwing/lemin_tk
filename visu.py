#!/usr/bin/env python3

from tkinter import *
from tooltip import *
from utils import *
from map_compressor import *

# update states
U_NONE = 0
U_WAIT = 1
U_REFRESH = 2
U_MOVE = 3
U_REDRAW = 4

# graphical constants # TODO: config structure
G_PRINT_GRID = True
G_SIDE_MIN = 10
G_SIDE_DEF = 50 # not used yet
G_SCREEN_DIV = 2 # use half the screen by default
G_FRAMEC_MIN = 10
G_FRAMEC_MAX = 500
G_FRAMEC_DEF = 100
G_FRAMEC_STEP = 10 # increment or decrement speed by this value
G_DELAY_DEF = 300 # wait time at each room
BACKGROUND_COLOR = "DodgerBlue3"
ROOM_COLOR = "blue"
START_ROOM_COLOR = "purple4"
END_ROOM_COLOR = "DarkGoldenrod1"
LINK_COLOR = "black"
ANT_COLOR = "red"

class vdata:
    def __init__(self, lmap, game):
        # window data
        self.win = Tk()
        self.screen_width = self.win.winfo_screenwidth()
        self.screen_height = self.win.winfo_screenheight()
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
        self.maxx = lmap.maxx - lmap.minx
        self.maxy = lmap.maxy - lmap.miny
        self.orig_w = self.maxx + 1
        self.orig_h = self.maxy + 1
        self.grid_w = self.orig_w
        self.grid_h = self.orig_h
        # biggest printable grid
        self.grid_w_max = (self.screen_width // G_SIDE_MIN) - 2
        self.grid_h_max = (self.screen_height // G_SIDE_MIN) - 2
        # smallest grid big enough to fit all rooms
        self.grid_w_min = 0
        self.grid_h_min = 0
        # graphical objects
        self.grid = []
        self.ants = []
        self.antn = lmap.antn
        self.links = []
        self.rooms = self.init_vrooms(lmap)
        self.roomn = lmap.size
        # update state
        self.update = U_NONE
        # asynchronous actions stack (FIFO)
        self.stack = []
        # movements
        self.framec = G_FRAMEC_DEF # number of frames by ant movement (speed)
        self.steps = [] # last room coordinates and x,y increments for each ant
        self.step = 0
        self.waitc = 0
        # game data
        self.start = lmap.start
        self.end = lmap.end
        self.game = game
        self.game_len = len(self.game)
        self.play = False
        self.turn = 0

    def init_vrooms(self, lmap):
        vrooms = {}
        for r in lmap.rooms:
            vrooms[r] = vroom(lmap.rooms[r], lmap.minx, lmap.miny)
        return vrooms
 
    def init_canvas(self):
        self.get_min_grid()
        if self.grid_w_max * self.grid_h_max < self.roomn:
            eprint("error: map too big for the screen")
            exit()
        elif self.grid_w_max < self.grid_w or self.grid_h_max < self.grid_h:
            compress_coordinates(self, compression="min")
        self.build_default_grid()
        win_w_min = (self.grid_w + 2) * G_SIDE_MIN
        win_h_min = (self.grid_h + 2) * G_SIDE_MIN
        self.win.minsize(win_w_min, win_h_min)

    def get_min_grid(self):
        scale = self.screen_width / self.screen_height
        while self.grid_w_min * self.grid_h_min < self.roomn:
            self.grid_w_min += 1
            self.grid_h_min = int(self.grid_w_min / scale)

    def build_default_grid(self):
        self.canvas_w = self.screen_width / G_SCREEN_DIV 
        self.canvas_h = self.screen_height / G_SCREEN_DIV 
        if self.build_canvas_grid():
            # if default window is not big enough
            self.canvas_w = (self.grid_w + 2) * G_SIDE_MIN
            self.canvas_h = (self.grid_h + 2) * G_SIDE_MIN
            self.build_canvas_grid()
        self.can = Canvas(self.win, width=self.canvas_w, height=self.canvas_h,\
        bg=BACKGROUND_COLOR)
        self.can.pack(side=TOP, fill=BOTH, expand=1)
        self.init_actions()
        self.can.update()

    def build_canvas_grid(self):
        self.side = min(self.canvas_w / (self.grid_w + 2),\
        self.canvas_h / (self.grid_h + 2))
        self.orig_x = (self.canvas_w - (self.grid_w * self.side)) / 2
        self.orig_y = (self.canvas_h - (self.grid_h * self.side)) / 2
        return 1 if self.side < G_SIDE_MIN else 0

    def init_actions(self):
        self.can.bind("<Configure>", self.configure_handler)
        self.win.bind("<space>", self.space_handler)
        self.win.bind("<Left>", self.left_handler)
        self.win.bind("<Right>", self.right_handler)
        self.win.bind("<Up>", self.up_handler)
        self.win.bind("<Down>", self.down_handler)
        self.win.bind("r", self.r_handler)
        self.win.bind("e", self.e_handler)
        self.win.bind("d", self.d_handler)
        
    def configure_handler(self, event):
        self.stack.insert(0, self.scale_canvas)
        self.redraw_w = event.width
        self.redraw_h = event.height

    def space_handler(self, event):
        self.stack.insert(0, self.play_pause)

    def left_handler(self, event):
        self.stack.insert(0, self.back_one_turn)

    def right_handler(self, event):
        self.stack.insert(0, self.forward_one_turn)

    def up_handler(self, event):
        self.stack.insert(0, self.speed_up)

    def down_handler(self, event):
        self.stack.insert(0, self.speed_down)

    def r_handler(self, event):
        self.stack.insert(0, self.reset)

    def e_handler(self, event):
        self.stack.insert(0, self.go_to_end)

    def d_handler(self, event):
        self.debug()

    def scale_canvas(self):
        self.update = U_REDRAW
        self.canvas_w = self.redraw_w
        self.canvas_h = self.redraw_h

    def play_pause(self):
        self.play = True if self.play == False else False

    def back_one_turn(self):
        if self.step > 0:
            self.step = 0
        elif self.turn > 0:
            self.turn -= 1
        self.play = False
        self.update = self.update_update(U_REFRESH)

    def forward_one_turn(self):
        if self.turn < self.game_len - 1:
            self.turn += 1
            self.play = False
            self.step = 0
            self.update = self.update_update(U_REFRESH)

    def reset(self):
        self.play = False
        self.step = 0
        self.turn = 0
        self.update = self.update_update(U_REFRESH)

    def go_to_end(self):
        self.play = False
        self.step = 0
        self.turn = self.game_len - 1
        self.update = self.update_update(U_REFRESH)

    def speed_up(self):
        if self.framec > G_FRAMEC_MIN:
            orig_framec = self.framec
            self.framec -= G_FRAMEC_STEP
            if self.step > 0 and self.turn < self.game_len - 1:
                self.step = (self.step / orig_framec) * self.framec
                self.update = self.update_update(U_MOVE)

    def speed_down(self):
        if self.framec < G_FRAMEC_MAX:
            orig_framec = self.framec
            self.framec += G_FRAMEC_STEP
            if self.step > 0:
                self.step = (self.step / orig_framec) * self.framec
                self.update = self.update_update(U_MOVE)

    def debug(self):
        print("self.turn:", self.turn, "/", self.game_len)
        print("self.step:", self.step)
        print("self.play:", "True" if self.play == True else "False")
        print("self.update:",\
        "U_NONE" if self.update == U_NONE else\
        "U_WAIT" if self.update == U_WAIT else\
        "U_REFRESH" if self.update == U_REFRESH else\
        "U_MOVE" if self.update == U_MOVE else\
        "U_REDRAW" if self.update == U_REDRAW else\
        "ERROR")
        print("len(self.stack)", len(self.stack))
        print("self.stack:", self.stack)

    def redraw(self):
        self.build_canvas_grid()
        self.draw_map()
        self.draw_ants()
        if self.step > 0:
            self.get_steps()
            self.draw_step()
    
    def draw_map(self):
        self.delete_map()
        if G_PRINT_GRID:
            self.draw_grid()
        for r in self.rooms:
            self.draw_links(r)
            self.draw_room(r)
        self.can.pack()
    
    # draw ants at current postition (according to self.turn)
    def draw_ants(self):
        self.delete_ants()
        for i in range(self.antn):
            r = self.game[self.turn][i]
            x1, y1, x2, y2 = self.ant_coords(self.rooms[r].x,\
            self.rooms[r].y)
            ant = self.can.create_oval(x1, y1, x2, y2, fill=ANT_COLOR)
            self.ants.append(ant)
        self.can.pack()
    
    def get_steps(self):
        self.steps.clear()
        for i in range(self.antn):
            # get the coordinates of the target room
            xy = self.ant_coords(\
            self.rooms[self.game[self.turn + 1][i]].x,\
            self.rooms[self.game[self.turn + 1][i]].y)
            # get the coordinates of the current room
            cur = self.ant_coords(\
            self.rooms[self.game[self.turn][i]].x,\
            self.rooms[self.game[self.turn][i]].y)
            # get increments
            ix = (xy[0] - cur[0]) / self.framec
            iy = (xy[1] - cur[1]) / self.framec
            self.steps.append([cur[0], cur[1], cur[2], cur[3], ix, iy])

    def draw_step(self):
        for i in range(self.antn):
            # move ant one frame toward the next node
            self.can.coords(self.ants[i],\
            self.steps[i][0] + (self.steps[i][4] * self.step),\
            self.steps[i][1] + (self.steps[i][5] * self.step),\
            self.steps[i][2] + (self.steps[i][4] * self.step),\
            self.steps[i][3] + (self.steps[i][5] * self.step))

    def fix(self):
        for i in range(self.antn):
            # fix ant precisely on the node
            xy = self.ant_coords(\
            self.rooms[self.game[self.turn][i]].x,\
            self.rooms[self.game[self.turn][i]].y)
            self.can.coords(self.ants[i], xy[0], xy[1], xy[2], xy[3])

    def delete_map(self):
        self.delete_grid()
        for r in self.rooms:
            self.can.delete(self.rooms[r].shape)
            self.rooms[r].shape = None
        for link in self.links:
            self.can.delete(link)
        self.links.clear()
    
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
    
    def draw_links(self, r):
        for l in self.rooms[r].links:
            if self.rooms[l].shape == None:
                x1, y1, x2, y2 = self.link_coords(self.rooms[r].x,\
                self.rooms[r].y, self.rooms[l].x, self.rooms[l].y)
                link = self.can.create_line(x1, y1, x2, y2,\
                fill=LINK_COLOR, width=self.side/15)
                self.links.append(link)
    
    def draw_room(self, r):
        x1, y1, x2, y2 = self.room_coords(self.rooms[r].x,\
        self.rooms[r].y)
        color = START_ROOM_COLOR if self.start == r\
        else END_ROOM_COLOR if self.end == r else ROOM_COLOR
        room = self.can.create_oval(x1, y1, x2, y2, fill=color, tags=r)
        CreateShapeToolTip(self.can, room, r)
        self.rooms[r].shape = room
    
    def delete_grid(self):
        for bar in self.grid:
            self.can.delete(bar)
        self.grid.clear()

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

    def delete_ants(self):
        for ant in self.ants:
            self.can.delete(ant)
        self.ants.clear()

    def play_game(self):
        self.async_actions()
        if self.play == True and self.update != U_WAIT:
            if self.turn < self.game_len - 1:
                self.step += 1
                if self.step == 1:
                    self.update = self.update_update(U_MOVE)
                elif self.step < self.framec:
                    self.update = self.update_update(U_REFRESH)
                else:
                    self.step = 0
                    self.turn += 1
                    self.update = self.update_update(U_REFRESH)
            else:
                self.play = False
        self.update_screen()
        self.win.after(1, self.play_game)

    def update_update(self, upid):
        return upid if self.update < upid else self.update

    def async_actions(self):
        while len(self.stack) > 0:
            af = self.stack.pop()
            af()

    def update_screen(self):
        if self.update == U_REDRAW:
            self.redraw()
            self.can.update()
            self.update = U_NONE
        elif self.update == U_MOVE:
            if self.step > 0:
                self.get_steps()
                self.draw_step()
            else:
                self.fix()
            self.can.update()
            self.update = U_NONE
        elif self.update == U_REFRESH:
            if self.step > 0:
                self.draw_step()
            else:
                self.fix()
                self.update = U_WAIT
                self.waitc = G_DELAY_DEF
            self.can.update()
        elif self.update == U_WAIT:
            if self.waitc > 0:
                self.waitc -= 1
            else:
                self.update = U_NONE

class vroom:
    def __init__(self, room, minx, miny):
        # grid coordinates
        self.orig_x = room.x
        self.orig_y = room.y
        self.x = room.x - minx # normalized x
        self.y = room.y - miny # normalized y
        # links to other rooms
        self.links = room.links.copy()
        # command attributes ("start", "end", etc...)
        self.attrs = room.attrs.copy()
        # graphical object
        self.shape = None

def run_visu(lmap, game):
    # init visual data
    vda = vdata(lmap, game)
    vda.init_canvas()

    # main loop
    vda.win.after(0, vda.play_game)
    vda.win.mainloop()
