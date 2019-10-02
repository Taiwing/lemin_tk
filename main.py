#!/usr/bin/env python3

from lemin_map_parser import *
from lemin_game_parser import *
from lemin_map_checker import *
from lemin_game_checker import *
from visu import *

lmap, lc = lemin_map_parser()
if lmap == None or lemin_map_checker(lmap):
    eprint("error: invalid map")
    exit()
game = lemin_game_parser(lmap, lc)
if game == None or lemin_game_checker(game, lmap):
    eprint("error: invalid solution")
    exit()
run_visu(lmap, game)
