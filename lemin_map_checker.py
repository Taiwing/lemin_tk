#!/usr/bin/env python3

from lemin_map import *

# apply a BFS to check if start and end are connected
def find_end(lmap, start, end):
    curlvl = [start]
    passed = []
    i = 0
    while curlvl:
        cur = curlvl.pop(0)
        passed.append(cur)
        for r in lmap.rooms[cur].links:
            if r not in passed and r not in curlvl:
                curlvl.append(r)
                if r == end:
                    return 1
    return 0

def lemin_map_checker(lmap):
    if lmap.antn <= 0:
        eprint("error: invalid number of ants")
        return 1
    if lmap.size < 2:
        eprint("error: there is less than two rooms")
        return 1
    if lmap.start == lmap.end:
        eprint("error: the start room is also the end room")
        return 1
    if find_end(lmap, lmap.start, lmap.end) == False:
        eprint("error: the start room and the end room are not connected")
        return 1
    return 0

