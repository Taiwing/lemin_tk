#!/usr/bin/env python3

from utils import *

def compress_coordinates(vda, compression="min", w_comp=0, h_comp=0):
    grid_w, grid_h = get_new_grid(vda, compression, w_comp, h_comp)
    scale_w = grid_w / vda.grid.orig_w
    scale_h = grid_h / vda.grid.orig_h
    vda.grid.width = grid_w
    vda.grid.height = grid_h
    grid = [[0] * vda.grid.height for i in range(vda.grid.width)] 
    for r in vda.lmap.rooms:
        x = int(vda.lmap.rooms[r].orig_x * scale_w)
        y = int(vda.lmap.rooms[r].orig_y * scale_h)
        if grid[x][y] != 0:
            x, y = move_room(vda, x, y, grid, 1)
        grid[x][y] = 1
        vda.lmap.rooms[r].x = x
        vda.lmap.rooms[r].y = y

def get_new_grid(vda, compression, w_comp, h_comp):
    grid_w = vda.grid.width_max
    grid_h = vda.grid.height_max
    if compression == "max":
        grid_w = vda.grid.width_min
        grid_h = vda.grid.height_min
        vda.grid.w_comp = 100
        vda.grid.h_comp = 100
    elif compression == "min":
        vda.grid.w_comp = (vda.grid.width / vda.grid.width_max)\
        / ((vda.grid.orig_w / vda.grid.width_min) / 100)
        vda.grid.h_comp = (vda.grid.height / vda.grid.height_max)\
        / ((vda.grid.orig_h / vda.grid.height_min) / 100)
    else:
        scale_w = ((vda.grid.orig_w / vda.grid.width_min) / 100) * w_comp
        scale_h = ((vda.grid.orig_h / vda.grid.height_min) / 100) * h_comp
        if scale_w >= 1:
            grid_w = int(vda.grid.orig_w / scale_w)
        if scale_h >= 1:
            grid_h = int(vda.grid.orig_h / scale_h)
        vda.grid.w_comp = w_comp
        vda.grid.h_comp = h_comp
    return grid_w, grid_h

def move_room(vda, x, y, grid, dist):
    start_y = y - dist
    start_x = x - dist
    end_y = y + dist
    end_x = x + dist
    if start_y < 0 and start_x < 0\
    and end_y > vda.grid.height - 1 and end_x > vda.grid.width - 1:
        eprint("error: no place found in grid")
        exit()
    ty = start_y 
    tx = max(0, start_x)
    if ty >= 0:
        while tx < end_x + 1 and tx < vda.grid.width:
            if grid[tx][ty] == 0:
                return tx, ty
            tx += 1
    ty = max(0, start_y)
    tx = end_x
    if tx < vda.grid.width:
        while ty < end_y + 1 and ty < vda.grid.height:
            if grid[tx][ty] == 0:
                return tx, ty
            ty += 1
    ty = end_y
    tx = min(vda.grid.width - 1, end_x)
    if ty < vda.grid.height:
        while tx >= start_x and tx >= 0:
            if grid[tx][ty] == 0:
                return tx, ty
            tx -= 1
    ty = min(vda.grid.height - 1, end_y)
    tx = start_x
    if tx >= 0:
        while ty >= start_y and ty >= 0:
            if grid[tx][ty] == 0:
                return tx, ty
            ty -= 1
    return move_room(vda, x, y, grid, dist + 1)
