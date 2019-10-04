#!/usr/bin/env python3

import sys
from os import system
from time import sleep

C_RED="\u001B[31m"
C_BLUE="\u001B[34m"
C_RESET="\u001B[0m"

if len(sys.argv) < 5:
    print("error: not enough arguments", file=sys.stderr)
    exit(1)

width = int(sys.argv[1])
height = int(sys.argv[2])
x = int(sys.argv[3])
y = int(sys.argv[4])

def clear():
    system("clear")

def print_grid(grid):
    for j in range(height):
        line = ""
        for i in range(width):
            line += grid[i][j]
        print(line)

def square_grid(turn, grid, s_x, s_y, width, height):
    dist = turn - 1
    color = C_BLUE if dist % 2 else C_RED
    start_x = s_x - dist
    start_y = s_y - dist
    end_x = s_x + dist
    end_y = s_y + dist
    if start_x < 0 and start_y < 0 and end_x > width - 1\
        and end_y > height - 1:
        return 0
    y = max(start_y, 0)
    while y < height and y < end_y + 1:
        x = max(start_x, 0)
        while x < width and x < end_x + 1:
            on_y = y == start_y or y == end_y
            on_x = x == start_x or x == end_x
            if on_y or on_x:
                grid[x][y] = color + str(dist % 10) + C_RESET
            x = x + 1 if on_y or x == end_x else end_x
        y += 1
    return turn + 1

grid = [["#" for j in range(height)] for i in range(width)]

turn = 1

while turn:
    clear()
    print_grid(grid)
    turn = square_grid(turn, grid, x, y, width, height)
    sleep(0.125)
