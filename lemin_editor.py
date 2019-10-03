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
        self.lscr.win.bind("p", self.p_handler)
        self.lscr.win.bind("r", self.r_handler)
        self.lscr.win.bind("u", self.u_handler)
        self.lscr.win.bind("d", self.d_handler)

    def left_handler(self, event):
        self.lscr.stack.insert(0, self.do_nothing)

    def right_handler(self, event):
        self.lscr.stack.insert(0, self.do_nothing)

    def up_handler(self, event):
        self.lscr.stack.insert(0, self.do_nothing)

    def down_handler(self, event):
        self.lscr.stack.insert(0, self.do_nothing)

    def p_handler(self, event):
        self.lscr.stack.insert(0, self.do_nothing)

    def r_handler(self, event):
        self.lscr.stack.insert(0, self.do_nothing)

    def u_handler(self, event):
        self.lscr.stack.insert(0, self.do_nothing)

    def d_handler(self, event):
        self.debug()

    # TODO: replace every do_nothing with a proper function
    def do_nothing(self): # TEMP
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


    ## update_screen functions ##
    def redraw(self):
        self.lscr.get_side_size()
        self.lscr.draw_map()
    
    def move(self):
        pass

    def refresh(self):
        pass

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
