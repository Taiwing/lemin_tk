#!/usr/bin/env python3

from lemin_map_parser import *
from lemin_game_parser import *
from lemin_map_checker import *
from lemin_game_checker import *
from lemin_player import *
from lemin_editor import *

if len(sys.argv) == 1:
    # try to read game from stdin
    lmap, lc = lemin_map_parser()
    if lmap == None or lemin_map_checker(lmap):
        eprint("error: invalid map")
        exit() # TODO: replace this with the main_menu when it is done
    game = lemin_game_parser(lmap, lc)
    if game == None or lemin_game_checker(game, lmap):
        eprint("error: invalid solution")
        exit() # TODO: replace this with the main_menu when it is done
    play_lemin_game(lmap, game)
else:
    map_file = open(sys.argv[1])
    lmap, lc = lemin_map_parser(map_file)
    map_file.close()
    if lmap == None or lemin_map_checker(lmap):
        eprint("error: invalid map")
        exit() # TODO: replace this with the main_menu when it is done
    #print(lmap.mprint())
    edit_lemin_map(lmap)
