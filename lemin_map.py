#!/usr/bin/env python3

from utils import *

def map_eprint(err):
    eprint("error: " + err)

class lemin_map:
    def __init__(self):
        self.antn = 0
        self.size = 0 # number of rooms
        self.rooms = {}
        self.links = {}
        self.start = ""
        self.end = ""
        self.orig_w = 0
        self.orig_h = 0

    def set_antn(self, antn, commands):
        commands.clear() #until antn commands are added if any
        if antn <= 0:
            map_eprint(str(ant) + " is an invalid number of ants")
            exit()
        self.antn = antn

    def add_room(self, r, commands, p):
        if r[0] in self.rooms:
            map_eprint("room \"" + r[0]  + "\" already defined.")
        else:
            self.rooms[r[0]] = room()
            self.size += 1
        self.rooms[r[0]].orig_x = r[1]
        if p.minx == None or r[1] < p.minx:
            p.minx = r[1]
        if p.maxx == None or r[1] > p.maxx:
            p.maxx = r[1]
        self.rooms[r[0]].orig_y = r[2]
        if p.miny == None or r[2] < p.miny:
            p.miny = r[2]
        if p.maxy == None or r[2] > p.maxy:
            p.maxy = r[2]
        for com in commands:
            # right now, this is ugly, do a function pointer dictionnary
            if com == "start":
                self.start = r[0]
                self.end = "" if self.end == self.start else self.end
                self.rooms[r[0]].attrs.append(com)
            elif com == "end":
                self.end = r[0]
                self.start = "" if self.start == self.end else self.start
                self.rooms[r[0]].attrs.append(com)
            elif com == "":
                map_eprint("empty command")
            else:
                map_eprint("\"" + com + "\" unknown command")

    def add_link(self, lnk, commands):
        commands.clear() #until link commands are a reality
        name = link_name(lnk[0], lnk[1])
        if lnk[0] not in self.rooms or lnk[1] not in self.rooms:
            map_eprint("\"" + lnk[0] + "-" + lnk[1] + "\" is invalid") 
            exit()
        elif name in self.links:
            map_eprint("\"" + lnk[0] + "-" + lnk[1] + "\" already exists") 
        else:
            self.links[name] = link()
            self.rooms[lnk[0]].links.append(lnk[1])
            self.rooms[lnk[1]].links.append(lnk[0])

    def mprint(self):
        ret = "antn = " + str(self.antn) + "\n"\
        + "size = " + str(self.size) + "\n"\
        + "start: " + self.start + "\n"\
        + "end: " + self.end + "\n"\
        + "\nrooms:\n"
        for room in self.rooms:
            ret += "\"" + room + "\":\n"
            ret += self.rooms[room].rprint()
        ret += "\nlinks:\n"
        for link in self.links:
            ret += link + "\n"
        return ret

class room:
    def __init__(self):
        # links to other rooms
        self.links = []
        # command attributes ("start", "end", etc...)
        self.attrs = []
        # for BFS verification of the map
        self.discovered = False 
        # grid coordinates
        self.orig_x = -1 # original normalized coordinates
        self.orig_y = -1 # original normalized coordinates
        self.x = -1 # current coordinates
        self.y = -1 # current coordinates
        # graphical object
        self.shape = None

    def rprint(self):
        ret = "orig_x = " + str(self.orig_x) +\
        "; orig_y = " + str(self.orig_y) + "\n"
        ret = "x = " + str(self.x) + "; y = " + str(self.y) + "\n"
        ret += "links: " + str(self.links) + "\n"
        ret += "attributes: " + str(self.attrs) + "\n"
        return ret

class link:
    def __init__(self):
        # graphical object
        self.shape = None

def link_name(a, b):
    if a < b:
        return a + "-" + b
    else:
        return b + "-" + a
