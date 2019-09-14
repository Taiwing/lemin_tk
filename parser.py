#!/usr/local/bin/python3

import * from colony.py

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
	#parse room and if it is valid return it
	if '-' not in s:
		spl = s.split(" "))
		if len(spl) == 3 and len(spl[0]) > 0:
			x = get_int(spl[1])
			y = get_int(spl[2])
			if x != None and y != None:
				return [spl[0], x, y], get_rooms
		parser_eprint("\"" + s "\" is not a valid room.", l)
		exit()
	else:
		#it should be a link
		return get_links(s, l), get_links

# 3rd part: get the links between the rooms
def get_links(s, l):
	if len(s) > 0:
		link = s.split('-')
		if len(link) == 2 and len(link[0]) > 0\
		and len(link[1]) > 0 and link[0] != link[1]:
			return link, get_links
		parser_eprint("\"" + s "\" is not a valid link.", l)
	else:
		#start getting moves
		return "\n", get_moves

# 4th part: get the moves from player, if any
def get_moves(s, l):
	#parse link and if it is valid return it
	return move, get_moves

def lemin_parser():
	l = 1
	commands = []
	col = colony()
	readf = get_antn

	for line in sys.stdin:
		s = line.strip("\n")
		t = get_types(s)
		if t == T_COMMAND:
			if s[2:] == "":
				parser_eprint("empty command", l)
			else:
				commands.append(s[2:])
		elif t == T_DATA:
			out, readf = readf(s, l)
			if readf == get_antn:
				col.set_antn(out, commands)
				readf = get_rooms
			elif readf == get_rooms:
				col.add_room(out, commands)
			elif readf == get_links:
				col.add_link(out, commands)
			elif readf == get_moves:
				col.add_move(out, commands)
		lc += 1
			
	
