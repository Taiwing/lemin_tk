#!/usr/bin/env python3

from lemin_window import *
from lemin_menu import *
from lemin_editor import *
from lemin_player import *

M_MENU = 1
M_EDITOR = 2
M_PLAYER = 3

class lemin_data:
    def __init__(self, command_line_mode):
        self.lwin = lemin_window()
        self.lwin.win.protocol("WM_DELETE_WINDOW", self.close_handler)
        self.mode = None
        self.data = None
        self.command_line_mode = command_line_mode

    def load_data(self, mode, lmap=None, game=None):
        self.mode = mode
        if self.mode == M_MENU:
            self.data = lemin_menu(self.lwin)
        elif self.mode == M_EDITOR:
            self.data = lemin_editor(self.lwin, lmap)
        elif self.mode == M_PLAYER:
            self.data = lemin_player(self.lwin, lmap, game)

    def switch_mode(self, new_mode, lmap=None, game=None):
#        if self.mode != M_MENU:
#            self.data.events.unbind()
        self.lwin.reset()
        self.data = self.load_data(new_mode, lmap, game)
        if new_mode != M_MENU:
            self.lwin.win.resizable(width=True, height=True)
            self.lwin.redrawf() #TODO: REMOVE THIS (OR AT LEAST MOVE IT)

    def close_handler(self):
        self.lwin.stack.clear()
        if self.mode != M_MENU and self.command_line_mode == False:
            self.lwin.stack.insert(0, self.return_to_menu)
        else:
            self.lwin.stack.insert(0, self.close)

    def close(self):
        self.lwin.win.destroy()
        self.lwin.win = None

    def return_to_menu(self):
        self.switch_mode(M_MENU)
