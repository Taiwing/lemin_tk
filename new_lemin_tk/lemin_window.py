#!/usr/bin/env python3

from tkinter import *

# update states
U_NONE = 0
U_WAIT = 1
U_REFRESH = 2
U_MOVE = 3
U_REDRAW = 4

class lemin_window:
    def __init__(self):
        # window data
        self.win = Tk()
        self.screen_width = self.win.winfo_screenwidth()
        self.screen_height = self.win.winfo_screenheight()
        self.win_w_min = 0
        self.win_h_min = 0
        # update state
        self.update = U_NONE
        # update functions
        self.redrawf = None
        self.movef = None
        self.refreshf = None
        self.waitf = None
        self.updatef = None
        # asynchronous actions stack (FIFO)
        self.stack = []

    def reset(self):
        slaves = self.win.pack_slaves()
        for s in slaves:
            s.destroy()
        self.load_drawf(None, None, None, None, None)

    def load_drawf(self, redrawf, movef, refreshf, waitf, updatef):
        self.redrawf = redrawf
        self.movef = movef
        self.refreshf = refreshf
        self.waitf = waitf
        self.updatef = updatef
    
    def update_update(self, upid):
        return upid if self.update < upid else self.update

    ## main loop functions ##
    def async_actions(self):
        while len(self.stack) > 0:
            af = self.stack.pop()
            af()

    def update_screen(self):
        if self.update == U_REDRAW:
            self.redrawf()
            self.updatef()
            self.update = U_NONE
        elif self.update == U_MOVE:
            self.movef()
            self.updatef()
            self.update = U_NONE
        elif self.update == U_REFRESH:
            self.refreshf()
            self.updatef()
        elif self.update == U_WAIT:
            self.waitf()
