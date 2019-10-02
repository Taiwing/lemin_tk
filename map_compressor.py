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
        lscr.grid.w_comp = w_comp
        lscr.grid.h_comp = h_comp
    return grid_w, grid_h

def move_room(lscr, x, y, grid, dist):
    start_y = y - dist
    start_x = x - dist
    end_y = y + dist
    end_x = x + dist
    if start_y < 0 and start_x < 0\
    and end_y > lscr.grid.height - 1 and end_x > lscr.grid.width - 1:
        eprint("error: no place found in grid")
        exit()
    ty = start_y 
    tx = max(0, start_x)
    if ty >= 0:
        while tx < end_x + 1 and tx < lscr.grid.width:
            if grid[tx][ty] == 0:
                return tx, ty
            tx += 1
    ty = max(0, start_y)
    tx = end_x
    if tx < lscr.grid.width:
        while ty < end_y + 1 and ty < lscr.grid.height:
            if grid[tx][ty] == 0:
                return tx, ty
            ty += 1
    ty = end_y
    tx = min(lscr.grid.width - 1, end_x)
    if ty < lscr.grid.height:
        while tx >= start_x and tx >= 0:
            if grid[tx][ty] == 0:
                return tx, ty
            tx -= 1
    ty = min(lscr.grid.height - 1, end_y)
    tx = start_x
    if tx >= 0:
        while ty >= start_y and ty >= 0:
            if grid[tx][ty] == 0:
                return tx, ty
            ty -= 1
    return move_room(lscr, x, y, grid, dist + 1)
