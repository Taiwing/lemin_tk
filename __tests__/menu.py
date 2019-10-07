#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk

BACKGROUND_COLOR = "DodgerBlue3"

class lemin_menu:
    def __init__(self):
        # window data
        self.win = Tk()
        self.screen_width = self.win.winfo_screenwidth()
        self.screen_height = self.win.winfo_screenheight()
        self.win_w = 300
        self.win_h = 500
        x, y = self.get_start_pos()
        self.win.geometry(str(self.win_w) + "x" + str(self.win_h) + "+"\
            + str(x) + "+" + str(y))
        self.win.resizable(width=False, height=False)
        # frame data
        self.frame = Frame(self.win, bg=BACKGROUND_COLOR)
        self.frame.pack(fill="both", expand=True)
        # label
        self.logo = Label(self.frame, text="LEMIN_TK",\
            font=("Helvetica", 48, "italic"),\
            fg="blue4", bg=BACKGROUND_COLOR,\
            padx=20, pady=20)
        self.logo.pack()
        # comboboxes
        self.combostyle = ttk.Style()
        self.combostyle.theme_create("combostyle", parent="alt",\
            settings = {"TCombobox":\
                        {"configure":\
#                            {"selectbackground": "blue",\
#                            "fieldbackground": "white",\
#                            "highlightbackground": BACKGROUND_COLOR,\
#                            "background": "white"}}})
                            {"highlightbackground": BACKGROUND_COLOR}}})
        self.combostyle.theme_use("combostyle")
        self.maps = ["map_a", "map_b", "map_c", "map_d"]
        self.select_map = ttk.Combobox(self.frame,\
            values=self.maps, state="readonly")
        self.select_map.pack()
        self.solvers = ["solver_a", "solver_b", "solver_c", "solver_d"]
        self.select_solver = ttk.Combobox(self.frame,\
            values=self.solvers, state="readonly")
        # buttons
        self.add_map_button = Button(self.frame, text="add map",\
            command=self.add_map, highlightbackground=BACKGROUND_COLOR,\
            padx=10, pady=10)
        self.add_map_button.pack()
        self.edit_map_button = Button(self.frame, text="edit map",\
            command=self.edit_map, highlightbackground=BACKGROUND_COLOR)
        self.edit_map_button.pack()
        self.generate_map_button = Button(self.frame, text="generate map",\
            command=self.generate_map, highlightbackground=BACKGROUND_COLOR,\
            padx=10, pady=10)
        self.generate_map_button.pack()
        self.select_solver.pack()
        self.add_solver_button = Button(self.frame, text="add solver",\
            command=self.add_solver, highlightbackground=BACKGROUND_COLOR,\
            padx=10, pady=10)
        self.add_solver_button.pack()
        self.play_button = Button(self.frame, text="play",\
            command=self.play, highlightbackground=BACKGROUND_COLOR)
        self.play_button.pack()

    def get_start_pos(self):
        x = (self.screen_width / 2) - (self.win_w / 2)
        y = (self.screen_height / 2) - (self.win_h / 2)
        return int(x), int(y)

    def add_map(self):
        print("add_map")

    def edit_map(self):
        print("edit_map")

    def generate_map(self):
        print("generate_map")

    def add_solver(self):
        print("add_solver")

    def play(self):
        print("play")
        

menu = lemin_menu()
menu.win.mainloop()
