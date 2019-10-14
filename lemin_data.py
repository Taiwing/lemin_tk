#!/usr/bin/env python3

from lemin_screen import *
from lemin_menu import *
from lemin_editor import *
from lemin_player import *

M_MENU = 1
M_EDITOR = 2
M_PLAYER = 3

class lemin_data:
    def __init__(self):
        self.lwin = lemin_window()
        self.mode = None
        self.data = None

    def load_data(self, mode, lmap=None, game=None):
        self.mode = mode
        if self.mode == M_MENU:
            self.data = lemin_menu(self.lwin)
        elif self.mode == M_EDITOR:
            self.data = lemin_editor(self.lwin, lmap)
        elif self.mode == M_PLAYER:
            self.data = lemin_player(self.lwin, lmap, game)

    def switch_mode(self, new_mode, lmap=None, game=None):
        #destroy everything in the window
        self.data = self.load_data(new_mode, lmap, game)
