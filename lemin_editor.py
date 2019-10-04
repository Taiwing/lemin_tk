#!/usr/bin/env python3

from lemin_screen import *
from lemin_map import *

# editor constants
E_GRID_WIDTH_DEF = 160
E_GRID_HEIGHT_DEF = 90

class lemin_editor:
    def __init__(self, lmap=None):
        if lmap == None:
            lmap = self.new_map()
        # lemin screen
        self.lscr = lemin_screen(lmap, self.redraw,\
        self.move, self.refresh, self.wait)
        self.lscr.init_canvas(self.init_editor_actions)
        self.lscr.win.after(0, self.edit_map)
        # edit data
        # cursor data
        self.cur_x = 0
        self.cur_y = 0
        self.cur = None

    def new_map(self):
        lmap = lemin_map()
        lmap.orig_w = E_GRID_WIDTH_DEF
        lmap.orig_h = E_GRID_HEIGHT_DEF
        return lmap

    ## event handling of lemin_editor ##
    def init_editor_actions(self):
        self.lscr.win.bind("<Left>", self.left_handler)
        self.lscr.win.bind("<Right>", self.right_handler)
        self.lscr.win.bind("<Up>", self.up_handler)
        self.lscr.win.bind("<Down>", self.down_handler)
        self.lscr.win.bind("s", self.s_handler)
        self.lscr.win.bind("e", self.e_handler)
        self.lscr.win.bind("r", self.r_handler)
        self.lscr.win.bind("l", self.l_handler)
        self.lscr.win.bind("u", self.u_handler)
        self.lscr.win.bind("d", self.d_handler)

    def left_handler(self, event):
        self.lscr.stack.insert(0, self.move_left)

    def right_handler(self, event):
        self.lscr.stack.insert(0, self.move_right)

    def up_handler(self, event):
        self.lscr.stack.insert(0, self.move_up)

    def down_handler(self, event):
        self.lscr.stack.insert(0, self.move_down)

    def s_handler(self, event):
        self.lscr.stack.insert(0, self.put_start)

    def e_handler(self, event):
        self.lscr.stack.insert(0, self.put_end)

    def r_handler(self, event):
        self.lscr.stack.insert(0, self.put_room)

    def l_handler(self, event):
        self.lscr.stack.insert(0, self.link)

    def u_handler(self, event):
        self.lscr.stack.insert(0, self.unlink)

    def d_handler(self, event):
        self.debug()

    def move_left(self):
        if self.cur_x > 0:
            self.cur_x -= 1
            self.lscr.update = self.lscr.update_update(U_REFRESH)

    def move_right(self):
        if self.cur_x < self.lscr.grid.width - 1:
            self.cur_x += 1
            self.lscr.update = self.lscr.update_update(U_REFRESH)

    def move_up(self):
        if self.cur_y > 0:
            self.cur_y -= 1
            self.lscr.update = self.lscr.update_update(U_REFRESH)

    def move_down(self):
        if self.cur_y < self.lscr.grid.height - 1:
            self.cur_y += 1
            self.lscr.update = self.lscr.update_update(U_REFRESH)

    def put_start(self):
        pass

    def put_end(self):
        pass
    
    def put_room(self):
        pass

    def link(self):
        pass

    def unlink(self):
        pass

    def debug(self):
        print("self.lscr.update:",\
        "U_NONE" if self.lscr.update == U_NONE else\
        "U_WAIT" if self.lscr.update == U_WAIT else\
        "U_REFRESH" if self.lscr.update == U_REFRESH else\
        "U_MOVE" if self.lscr.update == U_MOVE else\
        "U_REDRAW" if self.lscr.update == U_REDRAW else\
        "ERROR")
        print("len(self.lscr.stack)", len(self.lscr.stack))
        print("self.lscr.stack:", self.lscr.stack)
        print("self.lscr.grid.w_comp =", self.lscr.grid.w_comp)
        print("self.lscr.grid.h_comp =", self.lscr.grid.h_comp)

    ## drawing functions specific to lemin_editor  ##
    def cursor_coords(self, g_x, g_y):
        x, y = self.lscr.grid_to_graphical(g_x, g_y)
        return x - (self.lscr.side / 2), y - (self.lscr.side / 2),\
        x + (self.lscr.side / 2), y + (self.lscr.side / 2) 

    def draw_cursor(self):
        if self.cur != None:
            self.lscr.can.delete(self.cur)
        if self.cur_x >= self.lscr.grid.width\
        or self.cur_y >= self.lscr.grid.height:
            self.cur_x = 0
            self.cur_y = 0
        x1, y1, x2, y2 = self.cursor_coords(self.cur_x, self.cur_y)
        self.cur = self.lscr.can.create_rectangle(x1, y1, x2, y2, fill="red")

    def move_cursor(self):
        x1, y1, x2, y2 = self.cursor_coords(self.cur_x, self.cur_y)
        self.lscr.can.coords(self.cur, x1, y1, x2, y2)

    ## update_screen functions ##
    def redraw(self):
        self.lscr.get_side_size()
        self.lscr.draw_map()
        self.draw_cursor()
    
    def move(self):
        pass

    def refresh(self):
        self.move_cursor() # TODO: maybe move to move (lol) and use refresh for something else

    def wait(self):
        pass
    
    ## main loop function ##
    def edit_map(self):
        self.lscr.async_actions()
        self.lscr.update_screen()
        self.lscr.win.after(1, self.edit_map)

def edit_lemin_map(lmap):    
   e = lemin_editor(lmap) 
   e.lscr.win.mainloop()
