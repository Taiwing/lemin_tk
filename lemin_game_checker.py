#!/usr/bin/env python3

from lemin_map import *

def lemin_game_checker(game, lmap):
    l = len(game)
    rooms = {}
    for r in lmap.rooms:
        rooms[r] = 0
    rooms[lmap.start] = lmap.antn # at first every ant is in the starting room
    if l < 2:
        eprint("error: game too short")
        return 1
    for i in range(l):
        if len(game[i]) != lmap.antn:
            eprint("error: invalid solution")
            return 1
        if i > 0:
            for j in range(lmap.antn):
                cur = game[i][j]
                prev = game[i - 1][j]
                if cur != prev:
                    if cur not in lmap.rooms[prev].links:
                        eprint("error: \"" + cur + "\" and \"" + prev + "\" are not linked")
                        return 1
                    rooms[cur] += 1
                    rooms[prev] -= 1
                    if rooms[prev] < 0:
                        eprint("error: there was no ant in \"" + prev + "\"")
                        return 1
            for r in game[i]:
                if rooms[r] > 1 and r != lmap.start and r != lmap.end:
                    eprint("error: two ants in \"" + r + "\" at turn " + str(i))
                    return 1
    if rooms[lmap.end] < lmap.antn:
        eprint("error: not all ants made it to the end")
        return 1
    return 0
        

