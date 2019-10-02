#!/usr/bin/env python3

class lemin_grid:
    def __init__(self, lmap, screen_w, screen_h, G_SIDE_MIN):
        # grid before any modification
        self.orig_w = lmap.orig_w
        self.orig_h = lmap.orig_h
        # current grid
        self.width = self.orig_w
        self.height = self.orig_h
        # smallest grid big enough to fit all rooms
        self.width_min = 0
        self.height_min = 0
        # biggest printable grid
        self.big_width = (screen_w // G_SIDE_MIN) - 2
        self.big_height = (screen_h // G_SIDE_MIN) - 2
        # biggest grid for current map
        self.width_max = self.big_width if self.orig_w > self.big_width\
        else self.orig_w
        self.height_max = self.big_height if self.orig_h > self.big_height\
        else self.orig_h
        # compression values
        self.w_comp = 0
        self.h_comp = 0
        self.w_comp_min = 0
        self.h_comp_min = 0
        # graphical objects
        self.shapes = []
