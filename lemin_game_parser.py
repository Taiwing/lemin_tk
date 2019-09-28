#!/usr/bin/env python3

from lemin_map import *

def get_moves(s, l):
    spl = s.split(" ")
    moves = []
    i = 0
    while i < len(spl) and len(spl[i]) > 3 and spl[i][0] == 'L':
        move = []
        mv = spl[i][1:].split('-')
        if len(mv) != 2:
            break
        move.append(get_int(mv[0]))
        move.append(mv[1])
        if move[0] == None or move[1] == "":
            parser_eprint("\"" + s + "\" contains invalid moves.", l)
            return None
        moves.append(move)
        i += 1
    return moves

def check_moves(moves, lmap, l):
    for move in moves:
        if move[0] <= 0 or move[0] > lmap.antn:
            parser_eprint("\"" + move[0] + "\" is not a valid ant ID", l)
            return 1
        elif move[1] not in lmap.rooms:
            parser_eprint("non-existing room", l)
            return 1
    return 0

def lemin_game_parser(lmap, lc, source=sys.stdin):
    game = [[lmap.start] * lmap.antn]
    i = 0
    for line in source:
        s = line.strip("\n")
        moves = get_moves(s, lc)
        if moves == None or check_moves(moves, lmap, lc):
            return None
        game.append(game[i].copy())
        for move in moves:
            game[i + 1][move[0] - 1] = move[1]
        lc += 1
        i += 1
    return game
