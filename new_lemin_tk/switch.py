#!/usr/bin/env python3

from lemin_data import *

def switch(val=0, lmap=None, game=None, lda=None):
    if not hasattr(switch, "data"):
        switch.data = lda
    else:
        switch.data.switch_mode(val, lmap, game)
