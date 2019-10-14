#!/usr/bin/env python3

from utils import *

def compress_coordinates(lscr, compression="min", w_comp=0, h_comp=0):
    grid_w, grid_h = get_new_grid(lscr, compression, w_comp, h_comp)
    scale_w = grid_w / lscr.grid.orig_w
    scale_h = grid_h / lscr.grid.orig_h
    lscr.grid.width = grid_w
    lscr.grid.height = grid_h
    grid = [[0] * lscr.grid.height for i in range(lscr.grid.width)] 
    for r in lscr.lmap.rooms:
        x = int(lscr.lmap.rooms[r].orig_x * scale_w)
        y = int(lscr.lmap.rooms[r].orig_y * scale_h)
        if grid[x][y] != 0:
            x, y = move_room(lscr, x, y, grid, 1)
        grid[x][y] = 1
        lscr.lmap.rooms[r].x = x
        lscr.lmap.rooms[r].y = y

def get_new_grid(lscr, compression, w_comp, h_comp):
    grid_w = lscr.grid.width_max
    grid_h = lscr.grid.height_max
    if compression == "max":
        grid_w = lscr.grid.width_min
        grid_h = lscr.grid.height_min
        lscr.grid.w_comp = 100
        lscr.grid.h_comp = 100
    elif compression == "min":
        lscr.grid.w_comp = (lscr.grid.width / lscr.grid.width_max)\
        / ((lscr.grid.orig_w / lscr.grid.width_min) / 100)
        lscr.grid.h_comp = (lscr.grid.height / lscr.grid.height_max)\
        / ((lscr.grid.orig_h / lscr.grid.height_min) / 100)
    else:
        scale_w = ((lscr.grid.orig_w / lscr.grid.width_min) / 100) * w_comp
        scale_h = ((lscr.grid.orig_h / lscr.grid.height_min) / 100) * h_comp
        if scale_w >= 1:
            grid_w = int(lscr.grid.orig_w / scale_w)
        if scale_h >= 1:
            grid_h = int(lscr.grid.orig_h / scale_h)
        if grid_w * grid_h < lscr.roomn:
            grid_w = lscr.grid.width_min
            grid_y = lscr.grid.height_min
        lscr.grid.w_comp = w_comp
        lscr.grid.h_comp = h_comp
    return grid_w, grid_h

def move_room(lscr, s_x, s_y, grid, dist):
    start_x = s_x - dist
    start_y = s_y - dist
    end_x = s_x + dist
    end_y = s_y + dist
    if start_y < 0 and start_x < 0\
    and end_x > lscr.grid.width - 1\
    and end_y > lscr.grid.height - 1:
        eprint("error: no place found in grid")
        exit()
    y = max(start_y, 0)
    while y < lscr.grid.height and y < end_y + 1:
        x = max(start_x, 0)
        while x < lscr.grid.width and x < end_x + 1:
            on_y = y == start_y or y == end_y
            on_x = x == start_x or x == end_x
            if (on_y or on_x) and grid[x][y] == 0:
                return x, y
            x = x + 1 if on_y or x == end_x else end_x
        y += 1
    return move_room(lscr, s_x, s_y, grid, dist + 1)
