#!/usr/bin/env python3

from tkinter import *
from tooltip import *
from utils import *

# update states
U_NONE = 0
U_WAIT = 1
U_REFRESH = 2
U_MOVE = 3
U_REDRAW = 4

class vdata:
    def __init__(self, col):
        # grid data
        self.grid_w = 0
        self.grid_h = 0
        # screen data
        self.screen_w = 0
        self.screen_h = 0
        self.redraw_w = 0
        self.redraw_h = 0
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
        # wait time (ms)
        self.delay = 300
        self.waitc = 0
        # current coordinates and x,y increments for each ant
        self.steps = []
        self.step = 0
        # print grid option
        self.print_grid = True
        # copy of colony class for convenience
        self.col = col
        # play the game
        self.play = False
        # update state
        self.update = U_NONE
        # asynchronous actions stack (FIFO)
        self.stack = []

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
        self.init_actions()
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
        self.screen_w = self.redraw_w
        self.screen_h = self.redraw_h

    def play_pause(self):
        self.play = True if self.play == False else False

    def back_one_turn(self):
        if self.step > 0:
            self.step = 0
        elif self.col.turn > 0:
            self.col.turn -= 1
        self.play = False
        self.update = self.update_update(U_REFRESH)

    def forward_one_turn(self):
        if self.col.turn < len(self.col.game) - 1:
            self.col.turn += 1
            self.play = False
            self.step = 0
            self.update = self.update_update(U_REFRESH)

    def reset(self):
        self.play = False
        self.step = 0
        self.col.turn = 0
        self.update = self.update_update(U_REFRESH)

    def go_to_end(self):
        self.play = False
        self.step = 0
        self.col.turn = len(self.col.game) - 1
        self.update = self.update_update(U_REFRESH)

    def speed_up(self):
        if self.framec > 10:
            self.framec -= 10
            if self.step > 0 and self.col.turn < len(self.col.game) - 1:
                self.update = self.update_update(U_MOVE)

    def speed_down(self):
        if self.framec < 500:
            self.framec += 10
            if self.step > 0:
                self.update = self.update_update(U_MOVE)

    def debug(self):
        print("self.col.turn:", self.col.turn, "/", len(self.col.game))
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
        if self.build_canvas_grid(self.screen_w, self.screen_h):
            eprint("error: map too big for the screen")
            exit()
        self.draw_map()
        self.draw_ants()
        if self.step > 0:
            self.get_steps()
            self.draw_step()
        #not sure this else is needed (pretty sure it isnt) TODO: test
        else:
            self.fix()
    
    def draw_map(self):
        self.delete_map()
        if self.print_grid:
            self.draw_grid()
        for r in self.col.rooms:
            self.draw_links(r)
            self.draw_room(r)
        self.can.pack()
    
    # draw ants at current postition (according to self.col.turn)
    def draw_ants(self):
        self.delete_ants()
        for i in range(self.col.antn):
            r = self.col.game[self.col.turn][i]
            x1, y1, x2, y2 = self.ant_coords(self.col.rooms[r].x,\
            self.col.rooms[r].y)
            ant = self.can.create_oval(x1, y1, x2, y2, fill=self.ant_color)
            self.ants.append(ant)
        self.can.pack()
    
    def get_steps(self):
        self.steps.clear()
        for i in range(self.col.antn):
            # get the coordinates of the target room
            xy = self.ant_coords(\
            self.col.rooms[self.col.game[self.col.turn + 1][i]].x,\
            self.col.rooms[self.col.game[self.col.turn + 1][i]].y)
            # get the coordinates of the current room
            cur = self.ant_coords(\
            self.col.rooms[self.col.game[self.col.turn][i]].x,\
            self.col.rooms[self.col.game[self.col.turn][i]].y)
            # get increments
            ix = (xy[0] - cur[0]) / self.framec
            iy = (xy[1] - cur[1]) / self.framec
            self.steps.append([cur[0], cur[1], cur[2], cur[3], ix, iy])

    def draw_step(self):
        for i in range(self.col.antn):
            # move ant one frame toward the next node
            self.can.coords(self.ants[i],\
            self.steps[i][0] + (self.steps[i][4] * self.step),\
            self.steps[i][1] + (self.steps[i][5] * self.step),\
            self.steps[i][2] + (self.steps[i][4] * self.step),\
            self.steps[i][3] + (self.steps[i][5] * self.step))

    def fix(self):
        for i in range(self.col.antn):
            # fix ant precisely on the node
            xy = self.ant_coords(\
            self.col.rooms[self.col.game[self.col.turn][i]].x,\
            self.col.rooms[self.col.game[self.col.turn][i]].y)
            self.can.coords(self.ants[i], xy[0], xy[1], xy[2], xy[3])

    def delete_map(self):
        self.delete_grid()
        for r in self.rooms:
            self.can.delete(self.rooms[r])
        self.rooms.clear()
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
        for l in self.col.rooms[r].links:
            if l not in self.rooms:
                x1, y1, x2, y2 = self.link_coords(self.col.rooms[r].x,\
                self.col.rooms[r].y, self.col.rooms[l].x, self.col.rooms[l].y)
                link = self.can.create_line(x1, y1, x2, y2,\
                fill=self.link_color, width=self.side/15)
                self.links.append(link)
    
    def draw_room(self, r):
        x1, y1, x2, y2 = self.room_coords(self.col.rooms[r].x,\
        self.col.rooms[r].y)
        color = self.start_room_color if self.col.start == r\
        else self.end_room_color if self.col.end == r else self.room_color
        room = self.can.create_oval(x1, y1, x2, y2, fill=color, tags=r)
        CreateShapeToolTip(self.can, room, r)
        self.rooms[r] = room
    
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
            if self.col.turn < len(self.col.game) - 1:
                self.step += 1
                if self.step == 1:
                    self.update = self.update_update(U_MOVE)
                elif self.step < self.framec:
                    self.update = self.update_update(U_REFRESH)
                else:
                    self.step = 0
                    self.col.turn += 1
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
                self.waitc = self.delay
            self.can.update()
        elif self.update == U_WAIT:
            if self.waitc > 0:
                self.waitc -= 1
            else:
                self.update = U_NONE

def run_visu(col):
    # init visual data
    vda = vdata(col)
    col.normalize_coords()
    vda.init_screen()

    # main loop
    vda.win.after(0, vda.play_game)
    vda.win.mainloop()
