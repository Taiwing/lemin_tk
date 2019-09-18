#!/usr/local/bin/python3

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
        self.rooms[r[0]].y = r[2]
        for com in commands:
            # right now, this is ugly, do a function pointer dictionnary
            if com == "start":
                self.start = r[0]
                self.end = "" if self.end == self.start else self.end
            elif com == "end":
                self.end = r[0]
                self.start = "" if self.start == self.end else self.start
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
            else:
                self.turns.append(turn)

    def cprint(self):
        print("antn = " + str(self.antn))
        print("size = " + str(self.size))
        print("start: " + self.start)
        print("end: " + self.end)
        print("\nrooms:")
        for room in self.rooms:
            print("\"" + room + "\":")
            self.rooms[room].rprint()
        print("\nlinks:")
        for link in self.links:
            print(link)
        print("\nturns:")
        for turn in self.turns:
            print(turn)

class room:
    def __init__(self):
        # graphical coordinates if any
        self.x = -1
        self.y = -1
        # links to other rooms
        self.links = []
        # command attributes ("start", "end", etc...)
        self.attrs = []

    def rprint(self):
        print("x = " + str(self.x) + "; y = " + str(self.y))
        print("links: " + str(self.links))
        print("attributes: " + str(self.attrs))
