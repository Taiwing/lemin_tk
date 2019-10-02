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
    vda.grid.width_min = 0
    vda.grid.height_min = 0
    vda.grid.get_min(vda.screen_width, vda.screen_height, vda.roomn)

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
    vda.grid.width = vda.grid.orig_w
    vda.grid.height = vda.grid.orig_h
    vda.grid.w_comp = 0
    vda.grid.h_comp = 0
    vda.grid.width_min = 0
    vda.grid.height_min = 0
    vda.grid.get_min(vda.screen_width, vda.screen_height, vda.roomn)
    if vda.grid.big_width < vda.grid.width or vda.grid.big_height < vda.grid.height:
        compress_coordinates(vda, compression="min")
