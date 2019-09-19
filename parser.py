#!/usr/local/bin/python3

from colony import *

def parser_eprint(err, l):
    eprint("error: line " + str(l) + ": " + err)

def get_int(s):
    try:
        i = int(s)
        return i
    except ValueError:
        return None

# type of return from parsing functions
T_COMMAND = 1
T_COMMENT = 2
T_DATA = 0

# get the type of string (command, comment or data)
def get_type(s):
    if len(s) > 0:
        if s[:2] == "##":
            return T_COMMAND
        elif s[0] == '#':
            return T_COMMENT
    return T_DATA

# 1st part: get the number of ants
def get_antn(s, l):
    antn = get_int(s)
    if antn == None:
        parser_eprint("\"" + s + "\" is not a valid number of ants.", l)
        exit()
    return antn, get_antn

# 2nd part: get the rooms
def get_rooms(s, l):
    spl = s.split(" ")
    if len(spl) == 3 and len(spl[0]) > 0:
        x = get_int(spl[1])
        y = get_int(spl[2])
        if x == None or y == None:
            parser_eprint("\"" + s + "\" is not a valid room.", l)
            exit()
        return [spl[0], x, y], get_rooms
    else:
    #it should be a link
        return get_links(s, l)

# 3rd part: get the links between the rooms
def get_links(s, l):
    if len(s) > 0:
        link = s.split('-')
        if len(link) == 2 and len(link[0]) > 0\
        and len(link[1]) > 0 and link[0] != link[1]:
            return link, get_links
        parser_eprint("\"" + s + "\" is not a valid link.", l)
        exit()
    else:
        #start getting turns
        return "\n", get_turns

# 4th part: get the turns from player, if any
def get_turns(s, l):
    spl = s.split(" ")
    turn = []
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
            exit()
        turn.append(move)
        i += 1
    return turn, get_turns

def lemin_parser():
    lc = 1
    commands = []
    col = colony()
    readf = get_antn

    for line in sys.stdin:
        s = line.strip("\n")
        t = get_type(s)
        if t == T_COMMAND:
            if s[2:] == "":
                parser_eprint("empty command", l)
            else:
                commands.append(s[2:])
        elif t == T_DATA:
            out, readf = readf(s, lc)
            if readf == get_antn:
                col.set_antn(out, commands)
                readf = get_rooms
            elif readf == get_rooms:
                col.add_room(out, commands)
            elif readf == get_links:
                col.add_link(out, commands)
            elif readf == get_turns and out != '\n':
                col.add_turn(out, commands)
            commands.clear()
        lc += 1
    return col
