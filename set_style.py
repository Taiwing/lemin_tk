#!/usr/bin/env python3

from tkinter import ttk

BACKGROUND_COLOR = "DodgerBlue3"

app_style = None
def set_style():
    app_style = ttk.Style()
    app_style.theme_create("app_style", parent="alt",\
    settings = {
    "TCombobox": {"configure": {"highlightbackground": BACKGROUND_COLOR}},

    "TButton":       {"configure": {"font"            :("Calibri", 13),
                                    "background"      : "white",
                                    "foreground"      : "black",
                                    "padding"         : "6"},

                        "map"      : {"background"      : [("active", "#0556E2"),
                                ("disabled", "#8DBAE4")],
                                    "foreground"      : [("active", 'white'),
                                ("disabled", "grey")]}
    }})
    app_style.theme_use("app_style")
