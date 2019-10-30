#!/usr/bin/env python3

from map_compressor import *

def tag_used_rooms(game, rooms):
    for turn in game:
        for move in turn:
            if "used" not in rooms[move].attrs:
                rooms[move].attrs.append("used")

def remove_unused_rooms(lscr):
    unused = []
    for r in lscr.lmap.rooms:
        if "used" not in lscr.lmap.rooms[r].attrs:
            unused.append(r)
    for r in unused:
        lscr.lmap.unused_rooms[r] = lscr.lmap.rooms.pop(r)
    lscr.roomn = len(lscr.lmap.rooms)
    lscr.grid.width_min = 0
    lscr.grid.height_min = 0
    lscr.grid.get_min(lscr.lwin.screen_width, lscr.lwin.screen_height, lscr.roomn)

def restore_unused_rooms(lscr):
    unused = []
    for r in lscr.lmap.unused_rooms:
        unused.append(r)
    for r in unused:
        lscr.lmap.rooms[r] = lscr.lmap.unused_rooms.pop(r)
    lscr.roomn = len(lscr.lmap.rooms)
    for r in lscr.lmap.rooms:
        lscr.lmap.rooms[r].x = lscr.lmap.rooms[r].orig_x
        lscr.lmap.rooms[r].y = lscr.lmap.rooms[r].orig_y
    lscr.grid.width = lscr.grid.orig_w
    lscr.grid.height = lscr.grid.orig_h
    lscr.grid.width_min = 0
    lscr.grid.height_min = 0
    lscr.grid.get_min(lscr.lwin.screen_width, lscr.lwin.screen_height, lscr.roomn)
    if lscr.grid.w_comp != 0 and lscr.grid.h_comp != 0:
        compress_coordinates(lscr, "cust", lscr.grid.w_comp, lscr.grid.h_comp)
    if lscr.grid.big_width < lscr.grid.width or lscr.grid.big_height < lscr.grid.height:
        compress_coordinates(lscr, compression="min")
