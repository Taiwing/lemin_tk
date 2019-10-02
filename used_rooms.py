#!/usr/bin/env python3

from map_compressor import *

def tag_used_rooms(game, rooms):
    for turn in game:
        for move in turn:
            if "used" not in rooms[move].attrs:
                rooms[move].attrs.append("used")

def remove_unused_rooms(vda):
    unused = []
    for r in vda.lmap.rooms:
        if "used" not in vda.lmap.rooms[r].attrs:
            unused.append(r)
    for r in unused:
        vda.unused_rooms[r] = vda.lmap.rooms.pop(r)
    vda.roomn = len(vda.lmap.rooms)
    vda.grid_w_min = 0
    vda.grid_h_min = 0
    vda.get_min_grid()

def restore_unused_rooms(vda):
    unused = []
    for r in vda.unused_rooms:
        unused.append(r)
    for r in unused:
        vda.lmap.rooms[r] = vda.unused_rooms.pop(r)
    vda.roomn = len(vda.lmap.rooms)
    for r in vda.lmap.rooms:
        vda.lmap.rooms[r].x = vda.lmap.rooms[r].orig_x
        vda.lmap.rooms[r].y = vda.lmap.rooms[r].orig_y
    vda.grid_w = vda.orig_w
    vda.grid_h = vda.orig_h
    vda.w_comp = 0
    vda.h_comp = 0
    vda.grid_w_min = 0
    vda.grid_h_min = 0
    vda.get_min_grid()
    if vda.big_grid_w < vda.grid_w or vda.big_grid_h < vda.grid_h:
        compress_coordinates(vda, compression="min")
