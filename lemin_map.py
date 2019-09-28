#!/usr/bin/env python3

from utils import *

def map_eprint(err):
    eprint("error: " + err)

class lemin_map:
    def __init__(self):
        self.antn = 0
        self.size = 0 # number of rooms
        self.rooms = {}
        self.links = []
        self.start = ""
        self.end = ""
        self.minx = None
        self.maxx = None
        self.miny = None
        self.maxy = None

    def set_antn(self, antn, commands):
        commands.clear() #until antn commands are added if any
        if antn <= 0:
            map_eprint(str(ant) + " is an invalid number of ants")
            exit()
        self.antn = antn

    def add_room(self, r, commands):
        if r[0] in self.rooms:
            map_eprint("room \"" + r[0]  + "\" already defined.")
        else:
            self.rooms[r[0]] = room()
            self.size += 1
        self.rooms[r[0]].x = r[1]
        if self.minx == None or r[1] < self.minx:
            self.minx = r[1]
        if self.maxx == None or r[1] > self.maxx:
            self.maxx = r[1]
        self.rooms[r[0]].y = r[2]
        if self.miny == None or r[2] < self.miny:
            self.miny = r[2]
        if self.maxy == None or r[2] > self.maxy:
            self.maxy = r[2]
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

    def add_link(self, link, commands):
        commands.clear() #until link commands are a reality
        if link[0] not in self.rooms or link[1] not in self.rooms:
            map_eprint("\"" + link[0] + "-" + link[1] + "\" is invalid") 
            exit()
        elif link in self.links or link[::-1] in self.links:
            map_eprint("\"" + link[0] + "-" + link[1] + "\" already exists") 
        else:
            self.links.append(link)
            self.rooms[link[0]].links.append(link[1])
            self.rooms[link[1]].links.append(link[0])

    def mprint(self):
        ret = "antn = " + str(self.antn) + "\n"\
        + "size = " + str(self.size) + "\n"\
        + "start: " + self.start + "\n"\
        + "end: " + self.end + "\n"\
        + "minx = " + str(self.minx) + "\n"\
        + "maxx = " + str(self.maxx) + "\n"\
        + "miny = " + str(self.miny) + "\n"\
        + "maxy = " + str(self.maxy) + "\n"\
        + "\nrooms:\n"
        for room in self.rooms:
            ret += "\"" + room + "\":\n"
            ret += self.rooms[room].rprint()
        ret += "\nlinks:\n"
        for link in self.links:
            ret += str(link) + "\n"
        return ret

class room:
    def __init__(self):
        # grid coordinates
        self.x = -1
        self.y = -1
        # links to other rooms
        self.links = []
        # command attributes ("start", "end", etc...)
        self.attrs = []
        # for BFS verification of the map
        self.discovered = False 

    def rprint(self):
        ret = "x = " + str(self.x) + "; y = " + str(self.y) + "\n"
        ret += "links: " + str(self.links) + "\n"
        ret += "attributes: " + str(self.attrs) + "\n"
        return ret