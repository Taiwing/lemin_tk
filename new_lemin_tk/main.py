#!/usr/bin/env python3

from lemin_map_parser import *
from lemin_game_parser import *
from lemin_map_checker import *
from lemin_game_checker import *
from lemin_data import *

args = []
command_line_mode = 0
if len(sys.argv) > 1:
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "-c":
            command_line_mode = 1
        else:
            args.append(sys.argv[i])
        i += 1

mode = None
lmap = None
game = None
if command_line_mode:
    if len(args) == 0:
        lmap, lc = lemin_map_parser()
        if lmap == None or lemin_map_checker(lmap):
            eprint("error: invalid map")
            exit() # TODO: replace this with the main_menu when it is done
        game = lemin_game_parser(lmap, lc)
        if game == None or lemin_game_checker(game, lmap):
            eprint("error: invalid solution")
            exit() # TODO: replace this with the main_menu when it is done
        mode = M_PLAYER
    else:
        map_file = open(args[0])
        lmap, lc = lemin_map_parser(map_file)
        map_file.close()
        if lmap == None or lemin_map_checker(lmap):
            eprint("error: invalid map")
            exit() # TODO: replace this with the main_menu when it is done
        mode = M_EDITOR
else:
    mode = M_MENU

lda = lemin_data()
lda.load_data(mode, lmap, game)
lda.lwin.win.after(0, lda.data.mainf)
lda.lwin.win.mainloop()
