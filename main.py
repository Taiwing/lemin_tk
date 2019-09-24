#!/usr/bin/env python3

from parser import *
from visu import *

col = lemin_parser()
col.init_game()
#print(col.cprint())
run_visu(col)
