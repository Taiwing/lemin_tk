#!/usr/bin/env python3

from utils import *

def compress_coordinates(vda, compression="min", w_comp=0, h_comp=0):
    grid_w, grid_h = get_new_grid(vda, compression, w_comp, h_comp)
    scale_w = grid_w / vda.orig_w
    scale_h = grid_h / vda.orig_h
    vda.grid_w = grid_w
    vda.grid_h = grid_h
    grid = [[0] * vda.grid_h for i in range(vda.grid_w)] 
    for r in vda.rooms:
        x = int(vda.rooms[r].orig_x * scale_w)
        y = int(vda.rooms[r].orig_y * scale_h)
        if grid[x][y] != 0:
            x, y = move_room(vda, x, y, grid, 1)
        grid[x][y] = 1
        vda.rooms[r].x = x
        vda.rooms[r].y = y

def get_new_grid(vda, compression, w_comp, h_comp):
    grid_w = vda.grid_w_max
    grid_h = vda.grid_h_max
    if compression == "max":
        grid_w = vda.grid_w_min
        grid_h = vda.grid_h_min
        vda.w_comp = 100
        vda.h_comp = 100
    elif compression == "min":
        vda.w_comp = (vda.grid_w / vda.grid_w_max)\
        / ((vda.orig_w / vda.grid_w_min) / 100)
        vda.h_comp = (vda.grid_h / vda.grid_h_max)\
        / ((vda.orig_h / vda.grid_h_min) / 100)
    else:
        scale_w = ((vda.orig_w / vda.grid_w_min) / 100) * w_comp
        scale_h = ((vda.orig_h / vda.grid_h_min) / 100) * h_comp
        if scale_w >= 1:
            grid_w = int(vda.orig_w / scale_w)
        if scale_h >= 1:
            grid_h = int(vda.orig_h / scale_h)
        vda.w_comp = w_comp
        vda.h_comp = h_comp
    return grid_w, grid_h

def move_room(vda, x, y, grid, dist):
    start_y = y - dist
    start_x = x - dist
    end_y = y + dist
    end_x = x + dist
    if start_y < 0 and start_x < 0\
    and end_y > vda.grid_h - 1 and end_x > vda.grid_w - 1:
        eprint("error: no place found in grid")
        exit()
    ty = start_y 
    tx = max(0, start_x)
    if ty >= 0:
        while tx < end_x + 1 and tx < vda.grid_w:
            if grid[tx][ty] == 0:
                return tx, ty
            tx += 1
    ty = max(0, start_y)
    tx = end_x
    if tx < vda.grid_w:
        while ty < end_y + 1 and ty < vda.grid_h:
            if grid[tx][ty] == 0:
                return tx, ty
            ty += 1
    ty = end_y
    tx = min(vda.grid_w - 1, end_x)
    if ty < vda.grid_h:
        while tx >= start_x and tx >= 0:
            if grid[tx][ty] == 0:
                return tx, ty
            tx -= 1
    ty = min(vda.grid_h - 1, end_y)
    tx = start_x
    if tx >= 0:
        while ty >= start_y and ty >= 0:
            if grid[tx][ty] == 0:
                return tx, ty
            ty -= 1
    return move_room(vda, x, y, grid, dist + 1)
