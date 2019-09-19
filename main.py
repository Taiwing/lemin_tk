#!/usr/local/bin/python3

from parser import *
from visu import *

col = lemin_parser()
print(col.cprint())
run_visu(col)
