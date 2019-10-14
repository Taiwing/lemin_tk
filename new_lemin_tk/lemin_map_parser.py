#!/usr/bin/env python3

from lemin_map import *

# 1st part: get the number of ants
def get_antn(s, l):
    antn = get_int(s)
    if antn == None:
        parser_eprint("\"" + s + "\" is not a valid number of ants.", l)
        return None, None
    return antn, get_antn

# 2nd part: get the rooms
def get_rooms(s, l):
    spl = s.split(" ")
    if len(spl) == 3 and len(spl[0]) > 0:
        x = get_int(spl[1])
        y = get_int(spl[2])
        if x == None or y == None:
            parser_eprint("\"" + s + "\" is not a valid room.", l)
            return None, None
        return [spl[0], x, y], get_rooms
    else:
    # it should be a link
        return get_links(s, l)

# 3rd part: get the links between the rooms
def get_links(s, l):
    link = s.split('-')
    if len(link) == 2 and len(link[0]) > 0\
    and len(link[1]) > 0 and link[0] != link[1]:
        return link, get_links
    parser_eprint("\"" + s + "\" is not a valid link.", l)
    return None, None

def normalize_coordinates(rooms, p):
    for r in rooms:
        rooms[r].orig_x = rooms[r].orig_x - p.minx
        rooms[r].orig_y = rooms[r].orig_y - p.miny
        rooms[r].x = rooms[r].orig_x
        rooms[r].y = rooms[r].orig_y

def lemin_map_parser(source=sys.stdin):
    p = pdata()
    lc = 1
    commands = []
    lmap = lemin_map()
    readf = get_antn

    for line in source:
        line = line.strip("\n")
        if line == "":
            break
        elif line[:2] == "##":
                commands.append(line[2:])
        elif line[0] != '#':
            out, readf = readf(line, lc)
            if readf == get_antn:
                lmap.set_antn(out, commands)
                readf = get_rooms
            elif readf == get_rooms:
                lmap.add_room(out, commands, p)
            elif readf == get_links:
                lmap.add_link(out, commands)
            elif readf == None:
                return None, None
            commands.clear()
        lc += 1
    normalize_coordinates(lmap.rooms, p)
    if p.maxx != None and p.minx != None:
        lmap.orig_w = p.maxx - p.minx + 1
    if p.maxy != None and p.miny != None:
        lmap.orig_h = p.maxy - p.miny + 1
    return lmap, lc

class pdata:
    def __init__(self):
        self.minx = None
        self.maxx = None
        self.miny = None
        self.maxy = None
