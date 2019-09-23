#!/usr/bin/env python3

from utils import *

def col_eprint(err):
    eprint("error: " + err)

class colony:
    def __init__(self):
        self.antn = 0
        self.size = 0 #number of rooms
        self.rooms = {}
        self.links = []
        self.start = ""
        self.end = ""
        self.turns = []
        self.game = None
        self.turn = 0
        self.minx = None
        self.maxx = None
        self.miny = None
        self.maxy = None
        self.ants = []

    def set_antn(self, antn, commands):
        commands.clear() #until antn commands are added if any
        if antn <= 0:
            col_eprint(str(ant) + " is an invalid number of ants")
            exit()
        self.antn = antn

    def add_room(self, r, commands):
        if r[0] in self.rooms:
            col_eprint("room \"" + r[0]  + "\" already defined.")
        else:
            self.rooms[r[0]] = room()
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
            else:
                col_eprint("\"" + com + "\" unknown command")

    def add_link(self, link, commands):
        commands.clear() #until link commands are a reality
        if link[0] not in self.rooms or link[1] not in self.rooms:
            col_eprint("\"" + link[0] + "-" + link[1] + "\" is invalid") 
            exit()
        elif link in self.links or link[::-1] in self.links:
            col_eprint("\"" + link[0] + "-" + link[1] + "\" already exists") 
        else:
            self.links.append(link)
            self.rooms[link[0]].links.append(link[1])
            self.rooms[link[1]].links.append(link[0])

    def add_turn(self, turn, commands):
        commands.clear() #until turn commands are added
        for move in turn:
            if move[0] <= 0 or move[0] > self.antn:
                col_eprint("invalid ant ID")
                exit()
            elif move[1] not in self.rooms:
                col_eprint("non-existing room")
                exit()
        self.turns.append(turn)

    def cprint(self):
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
        ret += "\nturns:\n"
        for turn in self.turns:
            ret += str(turn) + "\n"
        ret += "game:\n"
        ret += str(self.game)
        return ret

    def normalize_coords(self):
        maxx = self.maxx - self.minx
        maxy = self.maxy - self.miny
        midy = maxy / 2
        for r in self.rooms:
            # make orignal coordinates 0,0    
            self.rooms[r].x = self.rooms[r].x - self.minx
            self.rooms[r].y = self.rooms[r].y - self.miny
            # invert the y axis
            dist = midy - self.rooms[r].y
            self.rooms[r].y = midy + dist
        self.maxx = maxx
        self.maxy = maxy
        self.minx = 0
        self.miny = 0

    def init_game(self):
        self.game = [[self.start]* self.antn for i in range(len(self.turns) + 1)]
        for i in range(len(self.turns)):
            for j in range(self.antn):
                self.game[i + 1][j] = self.game[i][j]
                for move in self.turns[i]:
                    if move[0] == j + 1:
                        self.game[i + 1][j] = move[1]
                        break

class room:
    def __init__(self):
        # graphical coordinates if any
        self.x = -1
        self.y = -1
        self.drawn = 0
        # links to other rooms
        self.links = []
        # command attributes ("start", "end", etc...)
        self.attrs = []

    def rprint(self):
        ret = "x = " + str(self.x) + "; y = " + str(self.y) + "\n"
        ret += "links: " + str(self.links) + "\n"
        ret += "attributes: " + str(self.attrs) + "\n"
        return ret
