#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import subprocess
from utils import *
from lemin_map_parser import *
from lemin_map_checker import *
from lemin_game_parser import *
from lemin_game_checker import *

BACKGROUND_COLOR = "DodgerBlue3"

class lemin_menu:
    def __init__(self, lwin):
        # window data
        self.lwin = lwin
        self.win_w = 300
        self.win_h = 500
        x, y = self.get_start_pos()
        self.lwin.win.geometry(str(self.win_w) + "x" + str(self.win_h) + "+"\
            + str(x) + "+" + str(y))
        self.lwin.win.resizable(width=False, height=False)
        # frame data
        self.frame = Frame(self.lwin.win, bg=BACKGROUND_COLOR)
        # label
        self.logo = Label(self.frame, text="LEMIN_TK",\
            font=("Helvetica", 48, "italic"),\
            fg="blue4", bg=BACKGROUND_COLOR)
        # comboboxes
        self.combostyle = ttk.Style()
        self.combostyle.theme_create("combostyle", parent="alt",\
            settings = {"TCombobox": {"configure":\
                        {"highlightbackground": BACKGROUND_COLOR}}})
        self.combostyle.theme_use("combostyle")
        self.maps = {}
        self.select_map = ttk.Combobox(self.frame, state="readonly")
        self.select_map.set("          -- select map --")
        self.solvers = {}
        self.select_solver = ttk.Combobox(self.frame, state="readonly")
        self.select_solver.set("        -- select solver --")
        # buttons
        self.add_map_button = Button(self.frame, text="add map",\
            command=self.add_map, highlightbackground=BACKGROUND_COLOR)
        self.new_map_button = Button(self.frame, text="new map",\
            command=self.new_map, highlightbackground=BACKGROUND_COLOR)
        self.edit_map_button = Button(self.frame, text="edit map",\
            command=self.edit_map, highlightbackground=BACKGROUND_COLOR,\
            state=DISABLED)
        self.generate_map_button = Button(self.frame, text="generate map",\
            command=self.generate_map, highlightbackground=BACKGROUND_COLOR,\
            state=DISABLED)
        self.add_solver_button = Button(self.frame, text="add solver",\
            command=self.add_solver, highlightbackground=BACKGROUND_COLOR)
        self.play_button = Button(self.frame, text="play",\
            command=self.play, highlightbackground=BACKGROUND_COLOR,\
            state=DISABLED)
        # packing
        self.frame.pack(fill="both", expand=True)
        self.logo.pack(padx=20, pady=20)
        self.select_map.pack(padx=10, pady=10)
        self.add_map_button.pack(padx=5, pady=5)
        self.new_map_button.pack(padx=5, pady=5)
        self.edit_map_button.pack(padx=5, pady=5)
        self.generate_map_button.pack(padx=5, pady=5)
        self.select_solver.pack(padx=10, pady=10)
        self.add_solver_button.pack(padx=5, pady=5)
        self.play_button.pack(padx=5, pady=5)

    def get_start_pos(self):
        x = (self.lwin.screen_width / 2) - (self.win_w / 2)
        y = (self.lwin.screen_height / 2) - (self.win_h / 2)
        return int(x), int(y)
        
    ## menu handlers ##
    def add_map_handler(self):
        self.lwin.stack.insert(0, self.add_map)
    
    def new_map_handler(self):
        self.lwin.stack.insert(0, self.new_map)
    
    def edit_map_handler(self):
        self.lwin.stack.insert(0, self.edit_map)
    
    def generate_map_handler(self):
        self.lwin.stack.insert(0, self.generate_map)
    
    def add_solver_handler(self):
        self.lwin.stack.insert(0, self.add_solver)
    
    def play_handler(self):
        self.lwin.stack.insert(0, self.play)

    ## menu functions ##
    def add_map(self):
        file_name = filedialog.askopenfilename(initialdir = "~",\
                title = "Select map")
        self.add_map_file(file_name)

    def add_map_file(self, file_name):
        if file_name != None and len(file_name) > 0:
            map_name = os.path.basename(file_name)
            if map_name not in self.maps:
                self.maps[map_name] = file_name
            elif self.maps[map_name] != file_name:
                self.maps[file_name] = file_name
                map_name = file_name
            else:
                eprint("error: map already loaded")
                return
            l = len(self.select_map["values"])
            if l > 0:
                self.select_map["values"] += (map_name,)
            else:
                self.select_map["values"] = (map_name)
                self.edit_map_button.configure(state=NORMAL)
            if self.play_button["state"] == DISABLED:
                if len(self.solvers) != 0:
                    self.play_button.configure(state=NORMAL)
            self.select_map.current(l)

    def edit_map(self):
        map_name = self.select_map.get()
        if map_name == None or len(map_name) == 0 or len(self.maps) == 0:
            eprint("error: no map selected")
            return
        map_file = open(self.maps[map_name])
        lmap, lc = lemin_map_parser(map_file)
        map_file.close()
        if lmap == None or lemin_map_checker(lmap):
            eprint("error: invalid map")
            return
        #TODO: switch to edit mode instead of this
        #file_name = edit_lemin_map(lmap)
        self.add_map_file(file_name)

    def new_map(self):
        #TODO: switch to edit mode instead of this
        #file_name = edit_lemin_map(None)
        self.add_map_file(file_name)

    def generate_map(self):
        pass

    def add_solver(self):
        file_name = filedialog.askopenfilename(initialdir = "~",\
                title = "Select solver")
        if file_name != None and len(file_name) > 0:
            solver_name = os.path.basename(file_name)
            if solver_name not in self.solvers:
                self.solvers[solver_name] = file_name
            elif self.solvers[solver_name] != file_name:
                self.solvers[file_name] = file_name
                solver_name = file_name
            else:
                eprint("error: solver already loaded")
                return
            l = len(self.select_solver["values"])
            if l > 0:
                self.select_solver["values"] += (solver_name,)
            else:
                self.select_solver["values"] = (solver_name)
            if self.play_button["state"] == DISABLED:
                if len(self.maps) != 0:
                    self.play_button.configure(state=NORMAL)
            self.select_solver.current(l)

    def play(self):
        map_name = self.select_map.get()
        solver_name = self.select_solver.get()
        if len(map_name) == 0 or len(solver_name) == 0\
                or len(self.maps) == 0 or len(self.solvers) == 0:
            eprint("error: no map or solver")
            return
        map_file = self.maps[map_name]
        solver_file = self.solvers[solver_name]
        proc = subprocess.run(solver_file + ' < ' + map_file,\
                stdout=subprocess.PIPE, shell=True)
        output = proc.stdout.decode("utf-8").splitlines(keepends=True)
        lmap, lc = lemin_map_parser(output)
        if lmap == None or lemin_map_checker(lmap):
            eprint("error: invalid map")
            return
        game = lemin_game_parser(lmap, lc, output[lc:])
        if game == None or lemin_game_checker(game, lmap):
            eprint("error: invalid solution")
            return
        #TODO: switch to player mode
    
    ## main loop function ##
    def mainf(self):
        self.lwin.async_actions()
        if self.lwin.win == None:
            return
        self.lwin.update_screen()
        self.lwin.win.after(1, self.mainf)
